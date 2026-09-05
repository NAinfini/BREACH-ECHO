# Unity 6.0 URP Compute Shader 통합 가이드

## 개요

Unity 6.0 URP RenderGraph에서 Compute Shader를 완전히 통합하여 GPU 컴퓨팅의 힘을 최대한 활용하는 방법을 다룹니다. GPU 기반 파티클 시스템부터 고급 포스트프로세싱, GPU Driven Culling까지, 실무에서 바로 적용할 수 있는 전문 기법들을 제공합니다.

## 목차

1. [RenderGraph Compute Pass 기본](#rendergraph-compute-pass-기본)
2. [GPU 기반 파티클 시스템](#gpu-기반-파티클-시스템)
3. [Compute Buffer 고급 관리](#compute-buffer-고급-관리)
4. [GPU Driven Culling 시스템](#gpu-driven-culling-시스템)
5. [Compute Shader 기반 포스트프로세싱](#compute-shader-기반-포스트프로세싱)
6. [AsyncGPUReadback 활용](#asyncgpureadback-활용)
7. [멀티패스 컴퓨트 파이프라인](#멀티패스-컴퓨트-파이프라인)
8. [성능 최적화 전략](#성능-최적화-전략)
9. [디버깅 및 프로파일링](#디버깅-및-프로파일링)
10. [실전 구현 예제](#실전-구현-예제)

---

## RenderGraph Compute Pass 기본

### 1. Compute Pass 생성 및 리소스 관리

```csharp
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using UnityEngine.Rendering.RenderGraphModule;

public class ComputeShaderRenderPass : ScriptableRenderPass
{
    private ComputeShader m_ComputeShader;
    private int m_KernelIndex;
    private const int THREAD_GROUP_SIZE_X = 8;
    private const int THREAD_GROUP_SIZE_Y = 8;
    
    public ComputeShaderRenderPass(ComputeShader computeShader)
    {
        m_ComputeShader = computeShader;
        m_KernelIndex = m_ComputeShader.FindKernel("CSMain");
        renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        ExecuteComputePass(renderGraph, resourceData, cameraData);
    }
    
    private void ExecuteComputePass(RenderGraph renderGraph, 
                                   UniversalResourceData resourceData,
                                   UniversalCameraData cameraData)
    {
        using (var builder = renderGraph.AddComputePass<ComputePassData>(
            "Custom Compute Pass", out var passData))
        {
            // 입력 텍스처
            passData.inputTexture = builder.ReadTexture(resourceData.activeColorTexture);
            
            // 출력 텍스처 생성
            var outputDesc = cameraData.cameraTargetDescriptor;
            outputDesc.enableRandomWrite = true; // UAV 활성화
            outputDesc.name = "Compute Output";
            passData.outputTexture = builder.WriteTexture(renderGraph.CreateTexture(outputDesc));
            
            // Compute Buffer 생성 및 바인딩
            var bufferDesc = new BufferDesc(1024, sizeof(float) * 4)
            {
                name = "Compute Buffer",
                type = GraphicsBuffer.Target.Structured
            };
            passData.computeBuffer = builder.WriteBuffer(renderGraph.CreateBuffer(bufferDesc));
            
            // 실행 함수 등록
            builder.SetRenderFunc<ComputePassData>((data, context) =>
            {
                ExecuteCompute(data, context, cameraData);
            });
            
            // 결과를 활성 컬러 텍스처로 복사
            CopyComputeResult(renderGraph, passData.outputTexture, resourceData);
        }
    }
    
    private void ExecuteCompute(ComputePassData data, ComputeGraphContext context, 
                               UniversalCameraData cameraData)
    {
        var cmd = context.cmd;
        
        // Compute Shader 설정
        cmd.SetComputeTextureParam(m_ComputeShader, m_KernelIndex, "_InputTexture", data.inputTexture);
        cmd.SetComputeTextureParam(m_ComputeShader, m_KernelIndex, "_OutputTexture", data.outputTexture);
        cmd.SetComputeBufferParam(m_ComputeShader, m_KernelIndex, "_ComputeBuffer", data.computeBuffer);
        
        // 상수 설정
        cmd.SetComputeVectorParam(m_ComputeShader, "_ScreenParams", 
            new Vector4(cameraData.cameraTargetDescriptor.width, 
                       cameraData.cameraTargetDescriptor.height, 0, 0));
        
        // Dispatch 계산
        int threadGroupsX = (cameraData.cameraTargetDescriptor.width + THREAD_GROUP_SIZE_X - 1) / THREAD_GROUP_SIZE_X;
        int threadGroupsY = (cameraData.cameraTargetDescriptor.height + THREAD_GROUP_SIZE_Y - 1) / THREAD_GROUP_SIZE_Y;
        
        // GPU 실행
        cmd.DispatchCompute(m_ComputeShader, m_KernelIndex, threadGroupsX, threadGroupsY, 1);
    }
}

// PassData 구조체
public struct ComputePassData
{
    public TextureHandle inputTexture;
    public TextureHandle outputTexture;
    public BufferHandle computeBuffer;
}
```

### 2. 기본 Compute Shader 템플릿

```hlsl
// ComputeShaderTemplate.compute
#pragma kernel CSMain

#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

// 스레드 그룹 크기 정의
[numthreads(8, 8, 1)]

// 입출력 리소스
Texture2D<float4> _InputTexture;
RWTexture2D<float4> _OutputTexture;
RWStructuredBuffer<float4> _ComputeBuffer;

// 상수 버퍼
float4 _ScreenParams; // (width, height, 1/width, 1/height)
float4 _ComputeParams;

void CSMain(uint3 id : SV_DispatchThreadID)
{
    // 경계 체크
    if (id.x >= (uint)_ScreenParams.x || id.y >= (uint)_ScreenParams.y)
        return;
    
    // UV 계산
    float2 uv = (id.xy + 0.5) * _ScreenParams.zw;
    
    // 입력 텍스처 샘플링
    float4 inputColor = _InputTexture[id.xy];
    
    // 커스텀 처리 로직
    float4 outputColor = ProcessPixel(inputColor, uv, id.xy);
    
    // 결과 저장
    _OutputTexture[id.xy] = outputColor;
    
    // 구조화 버퍼에도 데이터 저장 (필요시)
    uint bufferIndex = id.y * (uint)_ScreenParams.x + id.x;
    if (bufferIndex < 1024) // 버퍼 크기 체크
    {
        _ComputeBuffer[bufferIndex] = outputColor;
    }
}

// 커스텀 픽셀 처리 함수
float4 ProcessPixel(float4 inputColor, float2 uv, uint2 pixelCoord)
{
    // 예제: 단순한 색상 반전
    return 1.0 - inputColor;
}
```

---

## GPU 기반 파티클 시스템

### 1. GPU 파티클 시스템 구현

```csharp
using Unity.Collections;
using Unity.Collections.LowLevel.Unsafe;

// GPU 파티클 데이터 구조
[System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential)]
public struct GPUParticle
{
    public Vector3 position;
    public float life;
    public Vector3 velocity;
    public float size;
    public Vector4 color;
    public Vector3 acceleration;
    public float startLife;
}

public class GPUParticleSystem : ScriptableRenderPass
{
    private ComputeShader m_ParticleUpdateCompute;
    private ComputeShader m_ParticleEmitCompute;
    private Material m_ParticleRenderMaterial;
    
    private GraphicsBuffer m_ParticleBuffer;
    private GraphicsBuffer m_IndirectBuffer;
    private GraphicsBuffer m_CounterBuffer;
    
    private int m_UpdateKernel;
    private int m_EmitKernel;
    private int m_MaxParticles;
    
    private const int PARTICLE_THREAD_GROUP_SIZE = 64;
    
    public GPUParticleSystem(ComputeShader updateCompute, ComputeShader emitCompute, 
                            Material renderMaterial, int maxParticles = 100000)
    {
        m_ParticleUpdateCompute = updateCompute;
        m_ParticleEmitCompute = emitCompute;
        m_ParticleRenderMaterial = renderMaterial;
        m_MaxParticles = maxParticles;
        
        m_UpdateKernel = m_ParticleUpdateCompute.FindKernel("UpdateParticles");
        m_EmitKernel = m_ParticleEmitCompute.FindKernel("EmitParticles");
        
        InitializeBuffers();
        renderPassEvent = RenderPassEvent.AfterRenderingOpaques;
    }
    
    private void InitializeBuffers()
    {
        // 파티클 데이터 버퍼
        m_ParticleBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured, 
            m_MaxParticles, unsafe { sizeof(GPUParticle) });
        
        // Indirect Drawing Arguments 버퍼
        m_IndirectBuffer = new GraphicsBuffer(GraphicsBuffer.Target.IndirectArguments, 
            5, sizeof(uint));
        
        // 파티클 카운터 버퍼
        m_CounterBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured, 
            1, sizeof(uint));
        
        // 초기 Indirect Arguments 설정
        uint[] indirectArgs = { 0, 1, 0, 0, 0 }; // point topology
        m_IndirectBuffer.SetData(indirectArgs);
        
        // 카운터 초기화
        uint[] counterData = { 0 };
        m_CounterBuffer.SetData(counterData);
    }
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        // 1단계: 파티클 방출
        ExecuteParticleEmission(renderGraph, frameData);
        
        // 2단계: 파티클 업데이트
        ExecuteParticleUpdate(renderGraph, frameData);
        
        // 3단계: 파티클 렌더링
        ExecuteParticleRendering(renderGraph, resourceData, cameraData);
    }
    
    private void ExecuteParticleEmission(RenderGraph renderGraph, ContextContainer frameData)
    {
        using (var builder = renderGraph.AddComputePass<ParticleEmitPassData>(
            "Particle Emission", out var passData))
        {
            passData.particleBuffer = builder.WriteBuffer(renderGraph.ImportBuffer(m_ParticleBuffer));
            passData.counterBuffer = builder.WriteBuffer(renderGraph.ImportBuffer(m_CounterBuffer));
            
            builder.SetRenderFunc<ParticleEmitPassData>((data, context) =>
            {
                var cmd = context.cmd;
                
                // 방출 파라미터 설정
                cmd.SetComputeFloatParam(m_ParticleEmitCompute, "_DeltaTime", Time.deltaTime);
                cmd.SetComputeVectorParam(m_ParticleEmitCompute, "_EmitterPosition", Vector3.zero);
                cmd.SetComputeIntParam(m_ParticleEmitCompute, "_EmissionRate", 1000);
                
                // 버퍼 바인딩
                cmd.SetComputeBufferParam(m_ParticleEmitCompute, m_EmitKernel, "_ParticleBuffer", data.particleBuffer);
                cmd.SetComputeBufferParam(m_ParticleEmitCompute, m_EmitKernel, "_CounterBuffer", data.counterBuffer);
                
                // 방출 실행
                int threadGroups = (1000 + PARTICLE_THREAD_GROUP_SIZE - 1) / PARTICLE_THREAD_GROUP_SIZE;
                cmd.DispatchCompute(m_ParticleEmitCompute, m_EmitKernel, threadGroups, 1, 1);
            });
        }
    }
    
    private void ExecuteParticleUpdate(RenderGraph renderGraph, ContextContainer frameData)
    {
        using (var builder = renderGraph.AddComputePass<ParticleUpdatePassData>(
            "Particle Update", out var passData))
        {
            passData.particleBuffer = builder.WriteBuffer(renderGraph.ImportBuffer(m_ParticleBuffer));
            passData.counterBuffer = builder.ReadBuffer(renderGraph.ImportBuffer(m_CounterBuffer));
            passData.indirectBuffer = builder.WriteBuffer(renderGraph.ImportBuffer(m_IndirectBuffer));
            
            builder.SetRenderFunc<ParticleUpdatePassData>((data, context) =>
            {
                var cmd = context.cmd;
                
                // 물리 파라미터
                cmd.SetComputeFloatParam(m_ParticleUpdateCompute, "_DeltaTime", Time.deltaTime);
                cmd.SetComputeVectorParam(m_ParticleUpdateCompute, "_Gravity", Physics.gravity);
                cmd.SetComputeFloatParam(m_ParticleUpdateCompute, "_Damping", 0.98f);
                
                // 버퍼 바인딩
                cmd.SetComputeBufferParam(m_ParticleUpdateCompute, m_UpdateKernel, "_ParticleBuffer", data.particleBuffer);
                cmd.SetComputeBufferParam(m_ParticleUpdateCompute, m_UpdateKernel, "_CounterBuffer", data.counterBuffer);
                cmd.SetComputeBufferParam(m_ParticleUpdateCompute, m_UpdateKernel, "_IndirectBuffer", data.indirectBuffer);
                
                // 업데이트 실행
                int threadGroups = (m_MaxParticles + PARTICLE_THREAD_GROUP_SIZE - 1) / PARTICLE_THREAD_GROUP_SIZE;
                cmd.DispatchCompute(m_ParticleUpdateCompute, m_UpdateKernel, threadGroups, 1, 1);
            });
        }
    }
    
    private void ExecuteParticleRendering(RenderGraph renderGraph, 
                                        UniversalResourceData resourceData,
                                        UniversalCameraData cameraData)
    {
        using (var builder = renderGraph.AddRasterRenderPass<ParticleRenderPassData>(
            "Particle Rendering", out var passData))
        {
            passData.colorTarget = builder.UseColorBuffer(resourceData.activeColorTexture, 0);
            passData.depthTarget = builder.UseDepthBuffer(resourceData.activeDepthTexture, DepthAccess.ReadWrite);
            passData.particleBuffer = builder.ReadBuffer(renderGraph.ImportBuffer(m_ParticleBuffer));
            passData.indirectBuffer = builder.ReadBuffer(renderGraph.ImportBuffer(m_IndirectBuffer));
            
            builder.SetRenderFunc<ParticleRenderPassData>((data, context) =>
            {
                var cmd = context.cmd;
                
                // 렌더 상태 설정
                cmd.SetRenderTarget(data.colorTarget, data.depthTarget);
                
                // 머티리얼 프로퍼티 설정
                cmd.SetGlobalMatrix("_ViewMatrix", cameraData.GetViewMatrix());
                cmd.SetGlobalMatrix("_ProjectionMatrix", cameraData.GetProjectionMatrix());
                cmd.SetGlobalBuffer("_ParticleBuffer", data.particleBuffer);
                
                // Indirect 드로잉
                cmd.DrawProceduralIndirect(Matrix4x4.identity, m_ParticleRenderMaterial, 0, 
                    MeshTopology.Points, data.indirectBuffer);
            });
        }
    }
}

// PassData 구조체들
public struct ParticleEmitPassData
{
    public BufferHandle particleBuffer;
    public BufferHandle counterBuffer;
}

public struct ParticleUpdatePassData
{
    public BufferHandle particleBuffer;
    public BufferHandle counterBuffer;
    public BufferHandle indirectBuffer;
}

public struct ParticleRenderPassData
{
    public TextureHandle colorTarget;
    public TextureHandle depthTarget;
    public BufferHandle particleBuffer;
    public BufferHandle indirectBuffer;
}
```

### 2. GPU 파티클 업데이트 Compute Shader

```hlsl
// ParticleUpdate.compute
#pragma kernel UpdateParticles

#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

struct GPUParticle
{
    float3 position;
    float life;
    float3 velocity;
    float size;
    float4 color;
    float3 acceleration;
    float startLife;
};

[numthreads(64, 1, 1)]

RWStructuredBuffer<GPUParticle> _ParticleBuffer;
RWStructuredBuffer<uint> _CounterBuffer;
RWBuffer<uint> _IndirectBuffer;

float _DeltaTime;
float3 _Gravity;
float _Damping;

void UpdateParticles(uint3 id : SV_DispatchThreadID)
{
    uint particleIndex = id.x;
    uint maxParticles = _CounterBuffer[0];
    
    if (particleIndex >= maxParticles)
        return;
    
    GPUParticle particle = _ParticleBuffer[particleIndex];
    
    // 수명 감소
    particle.life -= _DeltaTime;
    
    if (particle.life <= 0)
    {
        // 파티클 죽음 - 카운터에서 제외
        InterlockedAdd(_IndirectBuffer[0], -1);
        return;
    }
    
    // 물리 시뮬레이션
    particle.acceleration += _Gravity;
    particle.velocity += particle.acceleration * _DeltaTime;
    particle.velocity *= _Damping;
    particle.position += particle.velocity * _DeltaTime;
    
    // 색상 변화 (수명에 따른 알파 감소)
    float lifeRatio = particle.life / particle.startLife;
    particle.color.a = lifeRatio;
    
    // 크기 변화
    particle.size = lerp(0.1, 1.0, lifeRatio);
    
    // 가속도 리셋
    particle.acceleration = float3(0, 0, 0);
    
    // 결과 저장
    _ParticleBuffer[particleIndex] = particle;
}
```

---

## Compute Buffer 고급 관리

### 1. 다중 버퍼 관리 시스템

```csharp
// 고급 Compute Buffer 관리자
public class AdvancedComputeBufferManager : IDisposable
{
    private Dictionary<string, ComputeBufferPool> m_BufferPools;
    private Dictionary<string, ComputeBufferBinding> m_ActiveBindings;
    
    // 버퍼 풀 클래스
    private class ComputeBufferPool
    {
        private Queue<GraphicsBuffer> m_AvailableBuffers;
        private List<GraphicsBuffer> m_AllBuffers;
        private int m_ElementCount;
        private int m_Stride;
        private GraphicsBuffer.Target m_Target;
        
        public ComputeBufferPool(int elementCount, int stride, GraphicsBuffer.Target target)
        {
            m_ElementCount = elementCount;
            m_Stride = stride;
            m_Target = target;
            m_AvailableBuffers = new Queue<GraphicsBuffer>();
            m_AllBuffers = new List<GraphicsBuffer>();
        }
        
        public GraphicsBuffer Rent()
        {
            if (m_AvailableBuffers.Count > 0)
            {
                return m_AvailableBuffers.Dequeue();
            }
            
            var buffer = new GraphicsBuffer(m_Target, m_ElementCount, m_Stride);
            m_AllBuffers.Add(buffer);
            return buffer;
        }
        
        public void Return(GraphicsBuffer buffer)
        {
            if (m_AllBuffers.Contains(buffer))
            {
                m_AvailableBuffers.Enqueue(buffer);
            }
        }
        
        public void Dispose()
        {
            foreach (var buffer in m_AllBuffers)
            {
                buffer?.Dispose();
            }
            m_AllBuffers.Clear();
            m_AvailableBuffers.Clear();
        }
    }
    
    // 버퍼 바인딩 정보
    private struct ComputeBufferBinding
    {
        public GraphicsBuffer buffer;
        public string shaderProperty;
        public int kernelIndex;
        public bool isReadOnly;
    }
    
    public AdvancedComputeBufferManager()
    {
        m_BufferPools = new Dictionary<string, ComputeBufferPool>();
        m_ActiveBindings = new Dictionary<string, ComputeBufferBinding>();
    }
    
    // 버퍼 풀 등록
    public void RegisterBufferPool<T>(string poolName, int elementCount, 
                                     GraphicsBuffer.Target target = GraphicsBuffer.Target.Structured) where T : unmanaged
    {
        if (m_BufferPools.ContainsKey(poolName)) return;
        
        int stride = unsafe { sizeof(T) };
        m_BufferPools[poolName] = new ComputeBufferPool(elementCount, stride, target);
    }
    
    // 버퍼 대여
    public GraphicsBuffer RentBuffer(string poolName)
    {
        if (m_BufferPools.TryGetValue(poolName, out var pool))
        {
            return pool.Rent();
        }
        return null;
    }
    
    // 버퍼 반납
    public void ReturnBuffer(string poolName, GraphicsBuffer buffer)
    {
        if (m_BufferPools.TryGetValue(poolName, out var pool))
        {
            pool.Return(buffer);
        }
    }
    
    // 자동 바인딩 시스템
    public void BindBufferToShader(ComputeShader shader, int kernelIndex, 
                                  string bufferName, string poolName, bool readOnly = false)
    {
        var buffer = RentBuffer(poolName);
        if (buffer == null) return;
        
        var binding = new ComputeBufferBinding
        {
            buffer = buffer,
            shaderProperty = bufferName,
            kernelIndex = kernelIndex,
            isReadOnly = readOnly
        };
        
        m_ActiveBindings[bufferName] = binding;
        
        // 셰이더에 바인딩
        shader.SetBuffer(kernelIndex, bufferName, buffer);
    }
    
    // 모든 바인딩 해제 및 반납
    public void UnbindAllBuffers()
    {
        foreach (var kvp in m_ActiveBindings)
        {
            var binding = kvp.Value;
            // 적절한 풀로 반납 (풀 이름 추적이 필요하면 binding에 추가)
            foreach (var pool in m_BufferPools.Values)
            {
                pool.Return(binding.buffer);
                break; // 첫 번째 풀에 반납 (실제로는 올바른 풀 찾기 필요)
            }
        }
        m_ActiveBindings.Clear();
    }
    
    // RenderGraph 통합
    public BufferHandle ImportToRenderGraph(RenderGraph renderGraph, string bufferName)
    {
        if (m_ActiveBindings.TryGetValue(bufferName, out var binding))
        {
            return renderGraph.ImportBuffer(binding.buffer);
        }
        return new BufferHandle();
    }
    
    public void Dispose()
    {
        UnbindAllBuffers();
        foreach (var pool in m_BufferPools.Values)
        {
            pool.Dispose();
        }
        m_BufferPools.Clear();
    }
}

// 사용 예제
public class ComputeBufferExample
{
    private AdvancedComputeBufferManager m_BufferManager;
    private ComputeShader m_ComputeShader;
    
    public void Initialize()
    {
        m_BufferManager = new AdvancedComputeBufferManager();
        
        // 다양한 타입의 버퍼 풀 등록
        m_BufferManager.RegisterBufferPool<Vector4>("ParticleData", 100000);
        m_BufferManager.RegisterBufferPool<Matrix4x4>("TransformData", 10000);
        m_BufferManager.RegisterBufferPool<uint>("IndexData", 50000, GraphicsBuffer.Target.Index);
        m_BufferManager.RegisterBufferPool<float>("FloatData", 1000000, GraphicsBuffer.Target.Structured);
    }
    
    public void ExecuteCompute()
    {
        int kernel = m_ComputeShader.FindKernel("ProcessData");
        
        // 자동 버퍼 바인딩
        m_BufferManager.BindBufferToShader(m_ComputeShader, kernel, "_ParticleBuffer", "ParticleData");
        m_BufferManager.BindBufferToShader(m_ComputeShader, kernel, "_TransformBuffer", "TransformData", true);
        
        // 컴퓨트 실행
        m_ComputeShader.Dispatch(kernel, 1000, 1, 1);
        
        // 바인딩 해제
        m_BufferManager.UnbindAllBuffers();
    }
}
```

---

## GPU Driven Culling 시스템

### 1. 계층적 GPU 컬링

```csharp
// GPU Driven Hierarchical Culling System
public class GPUHierarchicalCullingSystem : IDisposable
{
    private ComputeShader m_FrustumCullingCompute;
    private ComputeShader m_OcclusionCullingCompute;
    private ComputeShader m_LODComputeShader;
    
    private GraphicsBuffer m_InstanceBuffer;           // 렌더링할 인스턴스들
    private GraphicsBuffer m_BoundsBuffer;             // 바운딩 박스 정보
    private GraphicsBuffer m_VisibilityBuffer;         // 가시성 결과
    private GraphicsBuffer m_LODBuffer;                // LOD 레벨 정보
    private GraphicsBuffer m_IndirectArgsBuffer;       // Indirect Drawing Arguments
    
    // Hierarchical-Z Buffer for Occlusion Culling
    private RTHandle m_HierarchicalZBuffer;
    private int m_HiZMipLevels;
    
    [System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential)]
    public struct InstanceData
    {
        public Matrix4x4 objectToWorld;
        public Vector4 boundingSphere;     // xyz: center, w: radius  
        public Vector4 aabb;              // xyz: size, w: LOD bias
        public uint meshID;
        public uint materialID;
        public uint flags;                // visibility flags
        public uint _padding;
    }
    
    [System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential)]
    public struct CullingData
    {
        public Matrix4x4 viewMatrix;
        public Matrix4x4 projMatrix;
        public Vector4[] frustumPlanes;   // 6 planes
        public Vector4 cameraPosition;
        public Vector4 cullingParams;     // (maxDistance, lodBias, occlusionEnabled, _)
    }
    
    public GPUHierarchicalCullingSystem(ComputeShader frustumCulling, 
                                       ComputeShader occlusionCulling,
                                       ComputeShader lodCompute,
                                       int maxInstances)
    {
        m_FrustumCullingCompute = frustumCulling;
        m_OcclusionCullingCompute = occlusionCulling;
        m_LODComputeShader = lodCompute;
        
        InitializeBuffers(maxInstances);
        CreateHierarchicalZBuffer();
    }
    
    private void InitializeBuffers(int maxInstances)
    {
        m_InstanceBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured, 
            maxInstances, unsafe { sizeof(InstanceData) });
        
        m_BoundsBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured,
            maxInstances, sizeof(float) * 4); // AABB bounds
        
        m_VisibilityBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured,
            maxInstances, sizeof(uint));
        
        m_LODBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured,
            maxInstances, sizeof(uint));
        
        m_IndirectArgsBuffer = new GraphicsBuffer(GraphicsBuffer.Target.IndirectArguments,
            5 * 10, sizeof(uint)); // 최대 10개의 다른 메시에 대한 indirect args
    }
    
    private void CreateHierarchicalZBuffer()
    {
        var desc = new RenderTextureDescriptor
        {
            width = 1024,
            height = 1024,
            colorFormat = RenderTextureFormat.RFloat,
            dimension = TextureDimension.Tex2D,
            enableRandomWrite = true,
            autoGenerateMips = false,
            useMipMap = true
        };
        
        m_HiZMipLevels = Mathf.FloorToInt(Mathf.Log(Mathf.Max(desc.width, desc.height), 2)) + 1;
        desc.mipCount = m_HiZMipLevels;
        
        m_HierarchicalZBuffer = RTHandles.Alloc(desc, name: "Hierarchical Z Buffer");
    }
    
    // RenderGraph에서 실행되는 컬링 패스
    public void ExecuteCullingPass(RenderGraph renderGraph, UniversalCameraData cameraData,
                                  NativeArray<InstanceData> instanceData)
    {
        // 1단계: Instance 데이터 업데이트
        UpdateInstanceData(renderGraph, instanceData);
        
        // 2단계: Hierarchical Z 생성
        GenerateHierarchicalZ(renderGraph, cameraData);
        
        // 3단계: 프러스텀 컬링
        ExecuteFrustumCulling(renderGraph, cameraData);
        
        // 4단계: Occlusion 컬링  
        ExecuteOcclusionCulling(renderGraph, cameraData);
        
        // 5단계: LOD 계산
        ExecuteLODCalculation(renderGraph, cameraData);
        
        // 6단계: Indirect Args 생성
        GenerateIndirectArgs(renderGraph);
    }
    
    private void ExecuteFrustumCulling(RenderGraph renderGraph, UniversalCameraData cameraData)
    {
        using (var builder = renderGraph.AddComputePass<FrustumCullingPassData>(
            "GPU Frustum Culling", out var passData))
        {
            passData.instanceBuffer = builder.ReadBuffer(renderGraph.ImportBuffer(m_InstanceBuffer));
            passData.visibilityBuffer = builder.WriteBuffer(renderGraph.ImportBuffer(m_VisibilityBuffer));
            
            builder.SetRenderFunc<FrustumCullingPassData>((data, context) =>
            {
                var cmd = context.cmd;
                int kernel = m_FrustumCullingCompute.FindKernel("FrustumCulling");
                
                // 카메라 프러스텀 정보 설정
                var frustumPlanes = GeometryUtility.CalculateFrustumPlanes(cameraData.camera);
                var planeData = new Vector4[6];
                for (int i = 0; i < 6; i++)
                {
                    var plane = frustumPlanes[i];
                    planeData[i] = new Vector4(plane.normal.x, plane.normal.y, plane.normal.z, plane.distance);
                }
                
                cmd.SetComputeVectorArrayParam(m_FrustumCullingCompute, "_FrustumPlanes", planeData);
                cmd.SetComputeMatrixParam(m_FrustumCullingCompute, "_ViewMatrix", cameraData.GetViewMatrix());
                cmd.SetComputeMatrixParam(m_FrustumCullingCompute, "_ProjectionMatrix", cameraData.GetProjectionMatrix());
                cmd.SetComputeVectorParam(m_FrustumCullingCompute, "_CameraPosition", cameraData.worldSpaceCameraPos);
                
                // 버퍼 바인딩
                cmd.SetComputeBufferParam(m_FrustumCullingCompute, kernel, "_InstanceBuffer", data.instanceBuffer);
                cmd.SetComputeBufferParam(m_FrustumCullingCompute, kernel, "_VisibilityBuffer", data.visibilityBuffer);
                
                // 실행
                int threadGroups = (m_InstanceBuffer.count + 63) / 64;
                cmd.DispatchCompute(m_FrustumCullingCompute, kernel, threadGroups, 1, 1);
            });
        }
    }
    
    private void ExecuteOcclusionCulling(RenderGraph renderGraph, UniversalCameraData cameraData)
    {
        using (var builder = renderGraph.AddComputePass<OcclusionCullingPassData>(
            "GPU Occlusion Culling", out var passData))
        {
            passData.instanceBuffer = builder.ReadBuffer(renderGraph.ImportBuffer(m_InstanceBuffer));
            passData.visibilityBuffer = builder.WriteBuffer(renderGraph.ImportBuffer(m_VisibilityBuffer));
            passData.hiZBuffer = builder.ReadTexture(renderGraph.ImportTexture(m_HierarchicalZBuffer));
            
            builder.SetRenderFunc<OcclusionCullingPassData>((data, context) =>
            {
                var cmd = context.cmd;
                int kernel = m_OcclusionCullingCompute.FindKernel("OcclusionCulling");
                
                // Hi-Z 파라미터 설정
                cmd.SetComputeIntParam(m_OcclusionCullingCompute, "_HiZMipLevels", m_HiZMipLevels);
                cmd.SetComputeMatrixParam(m_OcclusionCullingCompute, "_ViewProjectionMatrix", 
                    cameraData.GetGPUProjectionMatrix() * cameraData.GetViewMatrix());
                
                // 버퍼 및 텍스처 바인딩
                cmd.SetComputeBufferParam(m_OcclusionCullingCompute, kernel, "_InstanceBuffer", data.instanceBuffer);
                cmd.SetComputeBufferParam(m_OcclusionCullingCompute, kernel, "_VisibilityBuffer", data.visibilityBuffer);
                cmd.SetComputeTextureParam(m_OcclusionCullingCompute, kernel, "_HiZBuffer", data.hiZBuffer);
                
                // 실행
                int threadGroups = (m_InstanceBuffer.count + 63) / 64;
                cmd.DispatchCompute(m_OcclusionCullingCompute, kernel, threadGroups, 1, 1);
            });
        }
    }
    
    public void Dispose()
    {
        m_InstanceBuffer?.Dispose();
        m_BoundsBuffer?.Dispose();
        m_VisibilityBuffer?.Dispose();
        m_LODBuffer?.Dispose();
        m_IndirectArgsBuffer?.Dispose();
        m_HierarchicalZBuffer?.Release();
    }
}

// PassData 구조체들
public struct FrustumCullingPassData
{
    public BufferHandle instanceBuffer;
    public BufferHandle visibilityBuffer;
}

public struct OcclusionCullingPassData
{
    public BufferHandle instanceBuffer;
    public BufferHandle visibilityBuffer;
    public TextureHandle hiZBuffer;
}
```

### 2. GPU 컬링 Compute Shader

```hlsl
// GPUCulling.compute
#pragma kernel FrustumCulling
#pragma kernel OcclusionCulling

#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

struct InstanceData
{
    float4x4 objectToWorld;
    float4 boundingSphere;    // xyz: center, w: radius
    float4 aabb;             // xyz: size, w: LOD bias  
    uint meshID;
    uint materialID;
    uint flags;
    uint _padding;
};

[numthreads(64, 1, 1)]

// 버퍼 및 상수
StructuredBuffer<InstanceData> _InstanceBuffer;
RWStructuredBuffer<uint> _VisibilityBuffer;
Texture2D<float> _HiZBuffer;
SamplerState sampler_HiZBuffer;

float4 _FrustumPlanes[6];
float4x4 _ViewMatrix;
float4x4 _ProjectionMatrix;
float4x4 _ViewProjectionMatrix;
float4 _CameraPosition;
int _HiZMipLevels;

// 프러스텀 컬링 커널
void FrustumCulling(uint3 id : SV_DispatchThreadID)
{
    uint instanceIndex = id.x;
    if (instanceIndex >= (uint)_InstanceBuffer.Length)
        return;
    
    InstanceData instance = _InstanceBuffer[instanceIndex];
    
    // 월드 공간 바운딩 스피어 중심 계산
    float3 worldCenter = mul(instance.objectToWorld, float4(instance.boundingSphere.xyz, 1.0)).xyz;
    float radius = instance.boundingSphere.w;
    
    // 각 프러스텀 평면에 대해 컬링 테스트
    bool isVisible = true;
    for (int i = 0; i < 6; i++)
    {
        float distance = dot(_FrustumPlanes[i].xyz, worldCenter) + _FrustumPlanes[i].w;
        if (distance < -radius)
        {
            isVisible = false;
            break;
        }
    }
    
    // 거리 기반 컬링
    float distanceToCamera = length(worldCenter - _CameraPosition.xyz);
    if (distanceToCamera > 1000.0) // 최대 거리
    {
        isVisible = false;
    }
    
    // 결과 저장 (1: 보임, 0: 컬링됨)
    _VisibilityBuffer[instanceIndex] = isVisible ? 1 : 0;
}

// Occlusion 컬링 커널
void OcclusionCulling(uint3 id : SV_DispatchThreadID)
{
    uint instanceIndex = id.x;
    if (instanceIndex >= (uint)_InstanceBuffer.Length)
        return;
    
    // 프러스텀 컬링을 통과한 것만 처리
    if (_VisibilityBuffer[instanceIndex] == 0)
        return;
    
    InstanceData instance = _InstanceBuffer[instanceIndex];
    
    // 월드 공간 바운딩 박스 계산
    float3 worldCenter = mul(instance.objectToWorld, float4(instance.boundingSphere.xyz, 1.0)).xyz;
    float3 worldSize = instance.aabb.xyz;
    
    // 바운딩 박스의 8개 꼭짓점을 클립 공간으로 변환
    float3 corners[8] = {
        worldCenter + float3(-worldSize.x, -worldSize.y, -worldSize.z) * 0.5,
        worldCenter + float3( worldSize.x, -worldSize.y, -worldSize.z) * 0.5,
        worldCenter + float3(-worldSize.x,  worldSize.y, -worldSize.z) * 0.5,
        worldCenter + float3( worldSize.x,  worldSize.y, -worldSize.z) * 0.5,
        worldCenter + float3(-worldSize.x, -worldSize.y,  worldSize.z) * 0.5,
        worldCenter + float3( worldSize.x, -worldSize.y,  worldSize.z) * 0.5,
        worldCenter + float3(-worldSize.x,  worldSize.y,  worldSize.z) * 0.5,
        worldCenter + float3( worldSize.x,  worldSize.y,  worldSize.z) * 0.5,
    };
    
    float2 minUV = float2(1, 1);
    float2 maxUV = float2(0, 0);
    float minDepth = 1;
    
    // 모든 꼭짓점을 스크린 공간으로 변환
    for (int i = 0; i < 8; i++)
    {
        float4 clipPos = mul(_ViewProjectionMatrix, float4(corners[i], 1.0));
        
        if (clipPos.w > 0)
        {
            float3 ndc = clipPos.xyz / clipPos.w;
            float2 screenUV = ndc.xy * 0.5 + 0.5;
            screenUV.y = 1.0 - screenUV.y; // UV 좌표계 변환
            
            minUV = min(minUV, screenUV);
            maxUV = max(maxUV, screenUV);
            minDepth = min(minDepth, ndc.z);
        }
    }
    
    // 스크린 밖에 있는 경우 통과
    if (minUV.x >= 1.0 || maxUV.x <= 0.0 || minUV.y >= 1.0 || maxUV.y <= 0.0)
        return;
    
    // UV 클램핑
    minUV = max(minUV, float2(0, 0));
    maxUV = min(maxUV, float2(1, 1));
    
    // 적절한 Hi-Z 밉 레벨 선택
    float2 size = maxUV - minUV;
    float maxSize = max(size.x, size.y);
    int mipLevel = clamp((int)log2(maxSize * 1024), 0, _HiZMipLevels - 1);
    
    // Hi-Z 테스트 (4개 코너 샘플링)
    float2 samplePoints[4] = {
        minUV,
        float2(maxUV.x, minUV.y),
        float2(minUV.x, maxUV.y),
        maxUV
    };
    
    float maxDepth = 0;
    for (int j = 0; j < 4; j++)
    {
        float depth = _HiZBuffer.SampleLevel(sampler_HiZBuffer, samplePoints[j], mipLevel).r;
        maxDepth = max(maxDepth, depth);
    }
    
    // Occlusion 테스트
    if (minDepth > maxDepth)
    {
        _VisibilityBuffer[instanceIndex] = 0; // Occluded
    }
}
```

이 Compute Shader 통합 가이드는 Unity 6.0 URP에서 GPU 컴퓨팅을 최대한 활용하여 고성능 렌더링 파이프라인을 구축하는 방법을 제공합니다. 특히 대규모 씬 렌더링과 복잡한 시뮬레이션에서 큰 성능 향상을 기대할 수 있습니다.

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "URP \uace0\uae09 \uac1c\ubc1c \uc601\uc5ed \ub204\ub77d \ubd84\uc11d", "status": "completed"}, {"content": "Compute Shader \ud1b5\ud569 \uac00\uc774\ub4dc \uc791\uc131", "status": "completed"}, {"content": "\uba54\uc778 \uac00\uc774\ub4dc \uc778\ub371\uc2a4 \uc5c5\ub370\uc774\ud2b8", "status": "in_progress"}]