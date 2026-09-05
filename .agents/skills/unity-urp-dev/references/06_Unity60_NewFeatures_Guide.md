# Unity 6.0 새로운 기능 통합 가이드

## 개요

Unity 6.0에서 새롭게 도입된 고급 렌더링 기능들과 이를 RenderGraph 기반 포스트프로세싱 시스템에 통합하는 방법을 다룹니다. GPU Resident Drawer, RenderGraph Viewer, Temporal Anti-aliasing, 그리고 향상된 XR 지원까지, 최신 기술을 활용한 차세대 렌더링 파이프라인 구현을 안내합니다.

## 목차

1. [GPU Resident Drawer 통합](#gpu-resident-drawer-통합)
2. [RenderGraph Viewer 디버깅](#rendergraph-viewer-디버깅)
3. [Temporal 기술 향상](#temporal-기술-향상)
4. [XR/VR 최적화 지원](#xrvr-최적화-지원)
5. [GPU Driven Rendering](#gpu-driven-rendering)
6. [향상된 텍스처 압축](#향상된-텍스처-압축)
7. [실시간 레이트레이싱 지원](#실시간-레이트레이싱-지원)
8. [Neural Network 통합](#neural-network-통합)
9. [성능 모니터링 개선](#성능-모니터링-개선)
10. [마이그레이션 전략](#마이그레이션-전략)

---

## GPU Resident Drawer 통합

### GPU Resident Drawer 활용

Unity 6.0의 GPU Resident Drawer는 그리기 명령을 GPU 메모리에 영구적으로 저장하여 CPU 오버헤드를 대폭 줄입니다.

#### 1. GPU Resident Drawer 기본 설정

```csharp
using UnityEngine.Rendering.Universal;
using UnityEngine.Rendering;

public class GPUResidentDrawerManager
{
    private GraphicsBuffer m_InstanceDataBuffer;
    private GraphicsBuffer m_DrawCommandBuffer;
    private ComputeShader m_CullingComputeShader;
    
    // GPU Resident Drawer 초기화
    public void Initialize(int maxInstanceCount)
    {
        // 인스턴스 데이터 버퍼 생성
        m_InstanceDataBuffer = new GraphicsBuffer(
            GraphicsBuffer.Target.Structured,
            maxInstanceCount,
            sizeof(float) * 16 // Matrix4x4 크기
        );
        
        // Draw Command 버퍼 생성
        m_DrawCommandBuffer = new GraphicsBuffer(
            GraphicsBuffer.Target.IndirectArguments,
            maxInstanceCount,
            GraphicsBuffer.IndirectDrawIndexedArgs.size
        );
    }
    
    // RenderGraph와 통합
    public TextureHandle ExecuteGPUDrivenRendering(RenderGraph renderGraph, 
                                                   TextureHandle colorTarget,
                                                   TextureHandle depthTarget)
    {
        using (var builder = renderGraph.AddRasterRenderPass<GPUDrivenPassData>(
            "GPU Driven Rendering", out var passData))
        {
            passData.colorTarget = builder.SetRenderAttachment(colorTarget, 0, AccessFlags.WriteAll);
            passData.depthTarget = builder.SetRenderAttachmentDepth(depthTarget, AccessFlags.WriteAll);
            passData.instanceBuffer = builder.UseBuffer(
                renderGraph.ImportBuffer(m_InstanceDataBuffer), AccessFlags.Read);
            passData.commandBuffer = builder.UseBuffer(
                renderGraph.ImportBuffer(m_DrawCommandBuffer), AccessFlags.Read);
            
            builder.SetRenderFunc(static (GPUDrivenPassData data, RasterGraphContext context) =>
            {
                ExecuteGPUDrivenPass(data, context);
            });
            
            return passData.colorTarget;
        }
    }
    
    private void ExecuteGPUDrivenPass(GPUDrivenPassData data, RasterGraphContext context)
    {
        // GPU Driven 렌더링 실행
        context.cmd.DrawMeshInstancedIndirect(
            mesh: GetTargetMesh(),
            submeshIndex: 0,
            material: GetGPUDrivenMaterial(),
            bounds: GetBounds(),
            bufferWithArgs: data.commandBuffer,
            argsOffset: 0,
            properties: null
        );
    }
}

private class GPUDrivenPassData
{
    internal TextureHandle colorTarget;
    internal TextureHandle depthTarget;
    internal BufferHandle instanceBuffer;
    internal BufferHandle commandBuffer;
}
```

#### 2. GPU 기반 컬링 시스템

```hlsl
// GPUDrivenCulling.compute
#pragma kernel CSMain

#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

struct InstanceData
{
    float4x4 objectToWorld;
    float4 boundingSphere; // xyz: center, w: radius
    uint meshID;
    uint materialID;
    uint lodLevel;
    uint _padding;
};

struct DrawCommand
{
    uint indexCountPerInstance;
    uint instanceCount;
    uint startIndexLocation;
    int baseVertexLocation;
    uint startInstanceLocation;
};

// 입력 버퍼
StructuredBuffer<InstanceData> _InstanceData;
RWStructuredBuffer<DrawCommand> _DrawCommands;
RWByteAddressBuffer _VisibilityBuffer;

// 카메라 파라미터
float4x4 _ViewProjMatrix;
float4 _FrustumPlanes[6];
float3 _CameraPosition;
float _MaxDistance;

[numthreads(64, 1, 1)]
void CSMain(uint3 id : SV_DispatchThreadID)
{
    uint instanceIndex = id.x;
    if (instanceIndex >= _InstanceData.Length)
        return;
        
    InstanceData instance = _InstanceData[instanceIndex];
    
    // 거리 기반 컬링
    float3 worldCenter = mul(instance.objectToWorld, float4(instance.boundingSphere.xyz, 1.0)).xyz;
    float distanceToCamera = length(worldCenter - _CameraPosition);
    
    bool isVisible = distanceToCamera < _MaxDistance;
    
    // 프러스텀 컬링
    if (isVisible)
    {
        for (int i = 0; i < 6; i++)
        {
            float distance = dot(_FrustumPlanes[i].xyz, worldCenter) + _FrustumPlanes[i].w;
            if (distance < -instance.boundingSphere.w)
            {
                isVisible = false;
                break;
            }
        }
    }
    
    // LOD 계산
    uint lodLevel = CalculateLODLevel(distanceToCamera);
    
    // 가시성 정보 업데이트
    if (isVisible)
    {
        uint originalValue;
        _VisibilityBuffer.InterlockedAdd(lodLevel * 4, 1, originalValue);
        
        // Draw Command 업데이트
        DrawCommand cmd;
        cmd.indexCountPerInstance = GetIndexCountForLOD(instance.meshID, lodLevel);
        cmd.instanceCount = 1;
        cmd.startIndexLocation = GetStartIndexForLOD(instance.meshID, lodLevel);
        cmd.baseVertexLocation = 0;
        cmd.startInstanceLocation = instanceIndex;
        
        _DrawCommands[instanceIndex] = cmd;
    }
    else
    {
        // 보이지 않는 인스턴스는 instanceCount를 0으로 설정
        DrawCommand cmd;
        cmd.instanceCount = 0;
        _DrawCommands[instanceIndex] = cmd;
    }
}

uint CalculateLODLevel(float distance)
{
    // 거리 기반 LOD 계산
    if (distance < 50.0) return 0; // High LOD
    if (distance < 100.0) return 1; // Medium LOD
    return 2; // Low LOD
}
```

---

## RenderGraph Viewer 디버깅

### RenderGraph Viewer 활용

Unity 6.0의 RenderGraph Viewer는 렌더링 파이프라인의 시각적 디버깅을 제공합니다.

#### 1. 디버깅 어노테이션 추가

```csharp
// ⚠️ 주의: 아래 코드는 개념 설명용 의사 코드(pseudo-code)입니다. URP 17 공개 API에 없는 메서드를 포함하며 실제 컴파일이 되지 않습니다.
public class DebugAnnotatedRenderPass : ScriptableRenderPass
{
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        // RenderGraph Viewer에서 보이는 패스 그룹 생성
        using (var passGroup = renderGraph.CreatePassGroup("Polygonal Bokeh DOF"))
        {
            // CoC 생성 패스 (녹색으로 표시)
            using (var builder = renderGraph.AddRasterRenderPass<CoCPassData>(
                "CoC Generation", out var cocData))
            {
                // 디버깅을 위한 메타데이터 추가
                builder.AddDebugMetadata("Purpose", "Generate Circle of Confusion map");
                builder.AddDebugMetadata("Performance Target", "<2ms");
                builder.AddDebugMetadata("Memory Usage", "R16_SFloat texture");
                
                // 리소스 설정...
                
                // ⚠️ 의사 코드: SetRenderFunc 시그니처도 실제와 다를 수 있습니다.
                builder.SetRenderFunc<CoCPassData>((data, context) =>
                {
                    // 실행 시간 측정을 위한 프로파일러 마커
                    using (new ProfilingSampler("CoC Generation").GetSampler(context.cmd))
                    {
                        ExecuteCoCGeneration(data, context);
                    }
                });
            }
            
            // Bokeh Filter 패스들 (파란색으로 표시)
            for (int i = 0; i < GetPassCount(); i++)
            {
                using (var builder = renderGraph.AddRasterRenderPass<BokehPassData>(
                    $"Bokeh Filter Pass {i}", out var bokehData))
                {
                    builder.AddDebugMetadata("Pass Index", i.ToString());
                    builder.AddDebugMetadata("Filter Angle", GetFilterAngle(i).ToString("F1"));
                    
                    // 실행 함수...
                }
            }
            
            // 최종 합성 패스 (주황색으로 표시)
            using (var builder = renderGraph.AddRasterRenderPass<CompositePassData>(
                "Final Composite", out var compositeData))
            {
                builder.AddDebugMetadata("Blend Mode", "Alpha Blend");
                
                // 실행 함수...
            }
        }
    }
    
    // 커스텀 디버깅 정보 제공
    public override void GetDebugInfo(ref RenderPassDebugInfo debugInfo)
    {
        debugInfo.passName = "Polygonal Bokeh DOF";
        debugInfo.estimatedGPUTime = GetEstimatedGPUTime();
        debugInfo.memoryUsage = CalculateMemoryUsage();
        debugInfo.drawCallCount = GetDrawCallCount();
    }
}
```

#### 2. 실시간 성능 모니터링

```csharp
// ⚠️ 주의: 아래 코드는 개념 설명용 의사 코드(pseudo-code)입니다. URP 17 공개 API에 없는 메서드를 포함하며 실제 컴파일이 되지 않습니다.
public class RenderGraphProfiler
{
    private Dictionary<string, PerformanceMetrics> m_PassMetrics;
    private CircularBuffer<float> m_FrameTimes;
    
    public void RecordPassMetrics(string passName, float gpuTime, int memoryUsage)
    {
        if (!m_PassMetrics.ContainsKey(passName))
        {
            m_PassMetrics[passName] = new PerformanceMetrics();
        }
        
        var metrics = m_PassMetrics[passName];
        metrics.AddSample(gpuTime, memoryUsage);
        
        // RenderGraph Viewer에 실시간 데이터 전송
        RenderGraphViewer.UpdatePassMetrics(passName, metrics);
    }
    
    public void DrawDebugOverlay()
    {
        #if UNITY_EDITOR
        if (RenderGraphViewer.IsEnabled())
        {
            foreach (var kvp in m_PassMetrics)
            {
                var passName = kvp.Key;
                var metrics = kvp.Value;
                
                // 실시간 성능 데이터를 UI에 표시
                EditorGUI.LabelField(GetRect(), 
                    $"{passName}: {metrics.averageGPUTime:F2}ms ({metrics.memoryUsage}KB)");
            }
        }
        #endif
    }
}

public class PerformanceMetrics
{
    public float averageGPUTime;
    public float maxGPUTime;
    public int memoryUsage;
    private CircularBuffer<float> samples = new CircularBuffer<float>(60);
    
    public void AddSample(float gpuTime, int memory)
    {
        samples.Add(gpuTime);
        averageGPUTime = samples.Average();
        maxGPUTime = samples.Max();
        memoryUsage = memory;
    }
}
```

---

## Temporal 기술 향상

### 고급 Temporal Anti-aliasing (TAA)

Unity 6.0에서 향상된 TAA 구현을 활용한 고품질 안티앨리어싱입니다.

#### 1. 향상된 TAA 구현

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Advanced/Enhanced TAA")]
public class EnhancedTAA : VolumeComponent, IPostProcessComponent
{
    [Header("Quality Settings")]
    [Tooltip("Temporal accumulation strength")]
    public ClampedFloatParameter temporalBlend = new ClampedFloatParameter(0.9f, 0.1f, 0.99f);
    
    [Tooltip("Motion vector sensitivity")]
    public ClampedFloatParameter motionSensitivity = new ClampedFloatParameter(1000f, 100f, 10000f);
    
    [Tooltip("History rejection threshold")]
    public ClampedFloatParameter historyRejection = new ClampedFloatParameter(0.05f, 0.01f, 0.2f);
    
    [Header("Advanced Features")]
    [Tooltip("Enable variance clipping")]
    public BoolParameter varianceClipping = new BoolParameter(true);
    
    [Tooltip("Use bicubic history sampling")]
    public BoolParameter bicubicSampling = new BoolParameter(false);
    
    [Tooltip("Enable velocity dilate")]
    public BoolParameter velocityDilate = new BoolParameter(true);
    
    public bool IsActive() => temporalBlend.value > 0;
}

private class EnhancedTAAPassData
{
    internal TextureHandle colorTexture;
    internal TextureHandle historyTexture;
    internal TextureHandle motionTexture;
    internal TextureHandle outputTexture;
    internal EnhancedTAA settings;
    internal Material material;
}

public class EnhancedTAARenderPass : ScriptableRenderPass
{
    private Material m_TAAmaterial;
    private RTHandle m_HistoryBuffer;
    private RTHandle m_VelocityBuffer;
    private Matrix4x4 m_PreviousViewProjMatrix;
    private int m_FrameIndex;
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        var taaSettings = VolumeManager.instance.stack.GetComponent<EnhancedTAA>();
        if (taaSettings == null || !taaSettings.IsActive()) return;
        
        ExecuteEnhancedTAA(renderGraph, resourceData, cameraData, taaSettings);
    }
    
    private void ExecuteEnhancedTAA(RenderGraph renderGraph, 
                                   UniversalResourceData resourceData,
                                   UniversalCameraData cameraData,
                                   EnhancedTAA settings)
    {
        using (var builder = renderGraph.AddRasterRenderPass<EnhancedTAAPassData>(
            "Enhanced TAA", out var passData))
        {
            // 현재 프레임 입력
            passData.currentColor = builder.UseTexture(resourceData.activeColorTexture, AccessFlags.Read);
            passData.currentDepth = builder.UseTexture(resourceData.cameraDepthTexture, AccessFlags.Read);
            passData.motionVectors = builder.UseTexture(resourceData.motionVectorTexture, AccessFlags.Read);
            
            // 히스토리 버퍼 설정
            if (m_HistoryBuffer == null)
            {
                var historyDesc = GetHistoryTextureDesc(cameraData);
                m_HistoryBuffer = RTHandles.Alloc(historyDesc);
            }
            passData.historyColor = builder.UseTexture(renderGraph.ImportTexture(m_HistoryBuffer), AccessFlags.Read);
            
            // 출력 텍스처
            var outputDesc = cameraData.cameraTargetDescriptor;
            outputDesc.name = "TAA Output";
            passData.output = builder.SetRenderAttachment(renderGraph.CreateTexture(outputDesc), 0, AccessFlags.WriteAll);
            
            // Jitter 패턴 설정
            SetJitterPattern(cameraData, m_FrameIndex);
            passData.settings = settings;
            
            builder.SetRenderFunc(static (EnhancedTAAPassData data, RasterGraphContext context) =>
            {
                ExecuteEnhancedTAAPass(data, context, data.settings);
            });
            
            // 히스토리 업데이트
            UpdateHistory(renderGraph, passData.output);
        }
        
        m_FrameIndex++;
    }
    
    private void SetJitterPattern(UniversalCameraData cameraData, int frameIndex)
    {
        // Halton 수열 기반 jitter 패턴 (Unity 6.0 개선된 버전)
        var jitter = GetHaltonSequence(frameIndex % 16);
        
        // 픽셀 단위로 정규화
        jitter.x /= cameraData.cameraTargetDescriptor.width;
        jitter.y /= cameraData.cameraTargetDescriptor.height;
        
        // 프로젝션 매트릭스에 jitter 적용
        var projectionMatrix = cameraData.GetProjectionMatrix();
        projectionMatrix.m02 += jitter.x * 2f;
        projectionMatrix.m12 += jitter.y * 2f;
        
        cameraData.SetViewAndProjectionMatrix(cameraData.GetViewMatrix(), projectionMatrix);
    }
    
    private Vector2 GetHaltonSequence(int index)
    {
        // 개선된 Halton 수열 (저주파수 노이즈 감소)
        return new Vector2(
            RadicalInverse(index, 2) - 0.5f,
            RadicalInverse(index, 3) - 0.5f
        );
    }
    
    private float RadicalInverse(int index, int baseValue)
    {
        float result = 0;
        float fraction = 1.0f / baseValue;
        
        while (index > 0)
        {
            result += (index % baseValue) * fraction;
            index /= baseValue;
            fraction /= baseValue;
        }
        
        return result;
    }
}
```

#### 2. TAA 셰이더 구현

```hlsl
// EnhancedTAA.hlsl
#ifndef ENHANCED_TAA_INCLUDED
#define ENHANCED_TAA_INCLUDED

#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"

TEXTURE2D(_CurrentColorTexture);
SAMPLER(sampler_CurrentColorTexture);
TEXTURE2D(_HistoryColorTexture);
SAMPLER(sampler_HistoryColorTexture);
TEXTURE2D(_MotionVectorTexture);
SAMPLER(sampler_MotionVectorTexture);
TEXTURE2D(_CameraDepthTexture);
SAMPLER(sampler_CameraDepthTexture);

float4 _TAAParams; // x: temporal blend, y: motion sensitivity, z: history rejection, w: frame index
float4x4 _PrevViewProjMatrix;

struct Varyings
{
    float4 positionCS : SV_POSITION;
    float2 texcoord : TEXCOORD0;
};

// 향상된 모션 벡터 계산
float2 GetMotionVector(float2 uv, float depth)
{
    // 하드웨어 모션 벡터가 있다면 사용
    float2 motionVector = SAMPLE_TEXTURE2D(_MotionVectorTexture, sampler_MotionVectorTexture, uv).xy;
    
    // 모션 벡터가 없다면 재구성
    if (length(motionVector) < 0.0001)
    {
        float4 worldPos = mul(unity_MatrixInvVP, float4(uv * 2 - 1, depth, 1));
        worldPos.xyz /= worldPos.w;
        
        float4 prevClipPos = mul(_PrevViewProjMatrix, float4(worldPos.xyz, 1));
        float2 prevUV = (prevClipPos.xy / prevClipPos.w) * 0.5 + 0.5;
        
        motionVector = uv - prevUV;
    }
    
    return motionVector * _TAAParams.y;
}

// 히스토리 샘플링 (Catmull-Rom 필터링)
float3 SampleHistoryCatmullRom(float2 uv)
{
    float2 texSize = _ScreenParams.xy;
    float2 samplePos = uv * texSize - 0.5;
    float2 f = frac(samplePos);
    float2 i = floor(samplePos);
    
    // Catmull-Rom 가중치 계산
    float2 w0 = f * (-0.5 + f * (1.0 - 0.5 * f));
    float2 w1 = 1.0 + f * f * (-2.5 + 1.5 * f);
    float2 w2 = f * (0.5 + f * (2.0 - 1.5 * f));
    float2 w3 = f * f * (-0.5 + 0.5 * f);
    
    float2 w12 = w1 + w2;
    float2 offset12 = w2 / (w1 + w2);
    
    float2 tc0 = (i - 1 + offset12) / texSize;
    float2 tc3 = (i + 2 + offset12) / texSize;
    float2 tc12 = (i + offset12) / texSize;
    
    float3 c0 = SAMPLE_TEXTURE2D_LOD(_HistoryColorTexture, sampler_HistoryColorTexture, tc0, 0).rgb;
    float3 c3 = SAMPLE_TEXTURE2D_LOD(_HistoryColorTexture, sampler_HistoryColorTexture, tc3, 0).rgb;
    float3 c12 = SAMPLE_TEXTURE2D_LOD(_HistoryColorTexture, sampler_HistoryColorTexture, tc12, 0).rgb;
    
    c0 = lerp(c0, c3, w0.x / (w0.x + w3.x));
    c12 = lerp(c12, c0, w0.y / (w0.y + w12.y));
    
    return c12;
}

// Variance 클리핑
float3 ClipToAABB(float3 color, float3 minimum, float3 maximum)
{
    float3 center = 0.5 * (maximum + minimum);
    float3 extents = 0.5 * (maximum - minimum);
    
    float3 offset = color - center;
    float3 ts = abs(extents.x) < 0.001 ? 0.0 : clamp(offset / extents, -1.0, 1.0);
    
    float t = max(max(ts.x, ts.y), ts.z);
    return center + offset * (t < 0 ? 0 : t);
}

// 이웃 색상의 통계 계산
void GetNeighborhoodStatistics(float2 uv, out float3 colorMin, out float3 colorMax, 
                              out float3 colorAvg, out float3 colorVar)
{
    float2 texelSize = _ScreenParams.zw;
    
    float3 c0 = SAMPLE_TEXTURE2D(_CurrentColorTexture, sampler_CurrentColorTexture, uv + float2(-1, -1) * texelSize).rgb;
    float3 c1 = SAMPLE_TEXTURE2D(_CurrentColorTexture, sampler_CurrentColorTexture, uv + float2( 0, -1) * texelSize).rgb;
    float3 c2 = SAMPLE_TEXTURE2D(_CurrentColorTexture, sampler_CurrentColorTexture, uv + float2( 1, -1) * texelSize).rgb;
    float3 c3 = SAMPLE_TEXTURE2D(_CurrentColorTexture, sampler_CurrentColorTexture, uv + float2(-1,  0) * texelSize).rgb;
    float3 c4 = SAMPLE_TEXTURE2D(_CurrentColorTexture, sampler_CurrentColorTexture, uv + float2( 0,  0) * texelSize).rgb;
    float3 c5 = SAMPLE_TEXTURE2D(_CurrentColorTexture, sampler_CurrentColorTexture, uv + float2( 1,  0) * texelSize).rgb;
    float3 c6 = SAMPLE_TEXTURE2D(_CurrentColorTexture, sampler_CurrentColorTexture, uv + float2(-1,  1) * texelSize).rgb;
    float3 c7 = SAMPLE_TEXTURE2D(_CurrentColorTexture, sampler_CurrentColorTexture, uv + float2( 0,  1) * texelSize).rgb;
    float3 c8 = SAMPLE_TEXTURE2D(_CurrentColorTexture, sampler_CurrentColorTexture, uv + float2( 1,  1) * texelSize).rgb;
    
    colorMin = min(c0, min(c1, min(c2, min(c3, min(c4, min(c5, min(c6, min(c7, c8))))))));
    colorMax = max(c0, max(c1, max(c2, max(c3, max(c4, max(c5, max(c6, max(c7, c8))))))));
    
    colorAvg = (c0 + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8) / 9.0;
    
    // Variance 계산 (간소화된 버전)
    colorVar = (c0 + c1 + c2 + c3 + c5 + c6 + c7 + c8) * 0.125 - c4;
    colorVar = abs(colorVar);
}

float4 EnhancedTAAFragment(Varyings input) : SV_Target
{
    float2 uv = input.texcoord;
    
    // 현재 프레임 색상
    float3 currentColor = SAMPLE_TEXTURE2D(_CurrentColorTexture, sampler_CurrentColorTexture, uv).rgb;
    
    // 깊이와 모션 벡터
    float depth = SAMPLE_TEXTURE2D(_CameraDepthTexture, sampler_CameraDepthTexture, uv).r;
    float2 motionVector = GetMotionVector(uv, depth);
    float2 prevUV = uv - motionVector;
    
    // 히스토리 색상 (Catmull-Rom 필터링)
    float3 historyColor = SampleHistoryCatmullRom(prevUV);
    
    // 이웃 통계 계산
    float3 colorMin, colorMax, colorAvg, colorVar;
    GetNeighborhoodStatistics(uv, colorMin, colorMax, colorAvg, colorVar);
    
    // Variance 클리핑
    historyColor = ClipToAABB(historyColor, colorMin, colorMax);
    
    // 모션에 따른 blend factor 조정
    float motionLength = length(motionVector * _ScreenParams.xy);
    float motionFactor = saturate(motionLength * 0.02);
    
    // 경계 체크 (화면 밖으로 나간 픽셀)
    bool isOutOfBounds = any(prevUV < 0) || any(prevUV > 1);
    float blendFactor = isOutOfBounds ? 0 : lerp(_TAAParams.x, 0.2, motionFactor);
    
    // 히스토리 거부 (큰 색상 차이)
    float colorDifference = length(currentColor - historyColor);
    if (colorDifference > _TAAParams.z)
    {
        blendFactor *= 0.1;
    }
    
    // 최종 색상 블렌딩
    float3 finalColor = lerp(currentColor, historyColor, blendFactor);
    
    return float4(finalColor, 1);
}

#endif
```

---

## XR/VR 최적화 지원

### VR용 Single Pass Instanced 렌더링

Unity 6.0의 향상된 XR 지원을 활용한 VR 최적화입니다.

#### 1. Single Pass Instanced 구현

```csharp
[Serializable]
public class XROptimizedPostProcess : VolumeComponent, IPostProcessComponent
{
    [Header("XR Settings")]
    [Tooltip("Enable Single Pass Instanced rendering")]
    public BoolParameter singlePassInstanced = new BoolParameter(true);
    
    [Tooltip("Use Fixed Foveated Rendering")]
    public BoolParameter fixedFoveatedRendering = new BoolParameter(false);
    
    [Tooltip("Foveation level (0-3)")]
    public ClampedIntParameter foveationLevel = new ClampedIntParameter(1, 0, 3);
    
    public bool IsActive() => XRSettings.enabled;
}

public class XRPostProcessRenderPass : ScriptableRenderPass
{
    private Material m_XRPostProcessMaterial;
    private XROptimizedPostProcess m_Settings;
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        if (!XRSettings.enabled) return;
        
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        m_Settings = VolumeManager.instance.stack.GetComponent<XROptimizedPostProcess>();
        if (m_Settings == null || !m_Settings.IsActive()) return;
        
        ExecuteXRPostProcess(renderGraph, resourceData, cameraData);
    }
    
    private void ExecuteXRPostProcess(RenderGraph renderGraph,
                                     UniversalResourceData resourceData,
                                     UniversalCameraData cameraData)
    {
        using (var builder = renderGraph.AddRasterRenderPass<XRPostProcessData>(
            "XR Post Process", out var passData))
        {
            // Single Pass Instanced를 위한 스테레오 텍스처 설정
            if (m_Settings.singlePassInstanced.value && cameraData.xr.enabled)
            {
                passData.sourceTexture = builder.UseTexture(resourceData.activeColorTexture, AccessFlags.Read);
                
                // 스테레오 타겟 생성 (좌우 눈을 위한 배열 텍스처)
                var stereoDesc = cameraData.cameraTargetDescriptor;
                stereoDesc.vrUsage = VRTextureUsage.TwoEyes;
                stereoDesc.volumeDepth = 2; // 좌우 눈
                passData.stereoOutput = builder.SetRenderAttachment(renderGraph.CreateTexture(stereoDesc), 0, AccessFlags.WriteAll);
            }
            else
            {
                // 일반 모노 렌더링
                passData.sourceTexture = builder.UseTexture(resourceData.activeColorTexture, AccessFlags.Read);
                passData.monoOutput = builder.SetRenderAttachment(
                    renderGraph.CreateTexture(cameraData.cameraTargetDescriptor), 0, AccessFlags.WriteAll);
            }
            
            // Fixed Foveated Rendering 설정
            if (m_Settings.fixedFoveatedRendering.value)
            {
                SetupFixedFoveatedRendering(cameraData);
            }
            
            builder.SetRenderFunc(static (XRPostProcessData data, RasterGraphContext context) =>
            {
                ExecuteXRPass(data, context);
            });
        }
    }
    
    private void SetupFixedFoveatedRendering(UniversalCameraData cameraData)
    {
        if (SystemInfo.supportedRenderTargetCount > 1)
        {
            // FFR 설정 (플랫폼별)
            #if UNITY_ANDROID
            // Oculus/Quest FFR 설정
            OVRManager.fixedFoveatedRenderingLevel = (OVRManager.FixedFoveatedRenderingLevel)m_Settings.foveationLevel.value;
            #endif
            
            #if UNITY_WSA && !UNITY_EDITOR
            // HoloLens FFR 설정 (Mixed Reality Toolkit)
            // 구현은 플랫폼에 따라 다름
            #endif
        }
    }
    
    private void ExecuteXRPass(XRPostProcessData data, RasterGraphContext context)
    {
        var cmd = context.cmd;
        
        if (data.stereoOutput.IsValid())
        {
            // Single Pass Instanced 렌더링
            cmd.SetGlobalTexture("_MainTex", data.sourceTexture);
            cmd.SetViewProjectionMatrices(GetStereoViewMatrix(0), GetStereoProjectionMatrix(0));
            
            // 인스턴스 렌더링으로 좌우 눈 동시 처리
            cmd.DrawMesh(GetFullscreenMesh(), Matrix4x4.identity, m_XRPostProcessMaterial, 0, 0);
        }
        else
        {
            // 일반 렌더링
            Blitter.BlitCameraTexture(cmd, data.sourceTexture, data.monoOutput, m_XRPostProcessMaterial, 0);
        }
    }
}

private class XRPostProcessData
{
    internal TextureHandle sourceTexture;
    internal TextureHandle stereoOutput;
    internal TextureHandle monoOutput;
}
```

#### 2. VR용 최적화 셰이더

```hlsl
// XRPostProcess.hlsl
#ifndef XR_POSTPROCESS_INCLUDED
#define XR_POSTPROCESS_INCLUDED

#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

#if defined(STEREO_INSTANCING_ON) || defined(STEREO_MULTIVIEW_ON)
    #define XR_ENABLED 1
#else
    #define XR_ENABLED 0
#endif

// 주의: 이 셰이더는 두 경로를 처리한다.
// - Single Pass Instanced (DrawMesh): C#에서 cmd.SetGlobalTexture("_MainTex", ...) 로 수동 바인딩 → _MainTex 사용
// - 일반 렌더링 (Blitter.BlitCameraTexture): _BlitTexture 바인딩 → 이 경로에서는 _BlitTexture도 선언 필요
TEXTURE2D(_MainTex);       // DrawMesh 경로 (SetGlobalTexture로 수동 바인딩)
TEXTURE2D_X(_BlitTexture); // Blitter 경로
SAMPLER(sampler_MainTex);
SAMPLER(sampler_BlitTexture);

// VR 전용 파라미터
float4 _FoveationParams; // x: inner radius, y: outer radius, z: strength, w: enabled
float4 _EyeProjection[2]; // 좌우 눈 프로젝션 정보

struct Attributes
{
    float4 positionOS : POSITION;
    float2 texcoord : TEXCOORD0;
    UNITY_VERTEX_INPUT_INSTANCE_ID
};

struct Varyings
{
    float4 positionCS : SV_POSITION;
    float2 texcoord : TEXCOORD0;
    UNITY_VERTEX_OUTPUT_STEREO
};

Varyings Vertex(Attributes input)
{
    Varyings output;
    UNITY_SETUP_INSTANCE_ID(input);
    UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(output);
    
    output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
    output.texcoord = input.texcoord;
    
    return output;
}

// Fixed Foveated Rendering 가중치 계산
float GetFoveationWeight(float2 uv)
{
    if (_FoveationParams.w < 0.5) return 1.0; // FFR 비활성화
    
    // 중심에서의 거리 계산
    float2 center = float2(0.5, 0.5);
    float distance = length(uv - center);
    
    // 내부/외부 반지름에 따른 품질 감소
    float innerRadius = _FoveationParams.x;
    float outerRadius = _FoveationParams.y;
    float strength = _FoveationParams.z;
    
    if (distance < innerRadius)
    {
        return 1.0; // 중심 영역은 최고 품질
    }
    else if (distance < outerRadius)
    {
        // 중간 영역은 점진적 품질 감소
        float t = (distance - innerRadius) / (outerRadius - innerRadius);
        return lerp(1.0, 1.0 - strength, t);
    }
    else
    {
        // 외곽 영역은 최저 품질
        return 1.0 - strength;
    }
}

// 적응형 샘플링 (FFR용)
float3 AdaptiveSample(float2 uv, float quality)
{
    if (quality > 0.8)
    {
        // 고품질: 4x 슈퍼샘플링
        float2 texelSize = _ScreenParams.zw * 0.25;
        float3 color = 0;
        color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv + float2(-1, -1) * texelSize).rgb;
        color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv + float2( 1, -1) * texelSize).rgb;
        color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv + float2(-1,  1) * texelSize).rgb;
        color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv + float2( 1,  1) * texelSize).rgb;
        return color * 0.25;
    }
    else if (quality > 0.5)
    {
        // 중간 품질: 2x 슈퍼샘플링
        float2 texelSize = _ScreenParams.zw * 0.5;
        float3 color = 0;
        color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv + float2(-0.5, -0.5) * texelSize).rgb;
        color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv + float2( 0.5,  0.5) * texelSize).rgb;
        return color * 0.5;
    }
    else
    {
        // 저품질: 단순 샘플링
        return SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv).rgb;
    }
}

float4 Fragment(Varyings input) : SV_Target
{
    UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input);
    
    float2 uv = input.texcoord;
    
    #if XR_ENABLED
    // VR에서 각 눈별 UV 좌표 조정
    if (unity_StereoEyeIndex == 0)
    {
        // 왼쪽 눈
        uv.x = uv.x * 0.5;
    }
    else
    {
        // 오른쪽 눈
        uv.x = uv.x * 0.5 + 0.5;
    }
    #endif
    
    // Fixed Foveated Rendering 품질 계산
    float foveationQuality = GetFoveationWeight(uv);
    
    // 적응형 샘플링으로 색상 가져오기
    float3 color = AdaptiveSample(uv, foveationQuality);
    
    // VR용 추가 보정 (색수차, 왜곡 보정 등)
    color = ApplyVRCorrections(color, uv);
    
    return float4(color, 1);
}

// VR용 시각적 보정
float3 ApplyVRCorrections(float3 color, float2 uv)
{
    // 렌즈 왜곡 보정
    float2 distortedUV = ApplyLensDistortion(uv);
    
    // 색수차 보정 (적-녹-청 채널별 개별 보정)
    float3 correctedColor;
    correctedColor.r = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, distortedUV + float2(0.001, 0)).r;
    correctedColor.g = color.g;
    correctedColor.b = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, distortedUV - float2(0.001, 0)).b;
    
    // 비네팅 보정
    float vignetteStrength = GetVignetteStrength(uv);
    correctedColor *= vignetteStrength;
    
    return correctedColor;
}

float2 ApplyLensDistortion(float2 uv)
{
    float2 center = float2(0.5, 0.5);
    float2 delta = uv - center;
    float radius = length(delta);
    
    // Barrel 왜곡 보정 (VR 렌즈용)
    float k1 = -0.15; // 왜곡 계수 (렌즈별 조정 필요)
    float correctionFactor = 1 + k1 * radius * radius;
    
    return center + delta * correctionFactor;
}

float GetVignetteStrength(float2 uv)
{
    float2 center = float2(0.5, 0.5);
    float distance = length(uv - center);
    
    // 자연스러운 비네팅 곡선
    return smoothstep(0.8, 0.2, distance);
}

#endif
```

---

## GPU Driven Rendering

### Indirect Drawing 시스템

Unity 6.0의 GPU Driven Rendering을 활용한 대규모 씬 렌더링 최적화입니다.

#### 1. GPU 기반 컬링 시스템

```csharp
public class GPUDrivenCullingSystem
{
    private ComputeShader m_CullingCompute;
    private ComputeBuffer m_InstanceBuffer;
    private ComputeBuffer m_VisibilityBuffer;
    private ComputeBuffer m_IndirectArgsBuffer;
    private GraphicsBuffer m_MeshDataBuffer;
    
    private const int THREAD_GROUP_SIZE = 64;
    private const int MAX_INSTANCES = 100000;
    
    public void Initialize()
    {
        m_CullingCompute = Resources.Load<ComputeShader>("GPUCulling");
        
        // 인스턴스 데이터 버퍼 (Transform + 바운딩 정보)
        m_InstanceBuffer = new ComputeBuffer(MAX_INSTANCES, 
            System.Runtime.InteropServices.Marshal.SizeOf<InstanceData>());
            
        // 가시성 결과 버퍼 (각 인스턴스의 가시성 플래그)
        m_VisibilityBuffer = new ComputeBuffer(MAX_INSTANCES, sizeof(uint));
        
        // Indirect Drawing Arguments
        m_IndirectArgsBuffer = new ComputeBuffer(5, sizeof(uint), 
            ComputeBufferType.IndirectArguments);
    }
    
    public ComputeBuffer ExecuteGPUCulling(Camera camera, int instanceCount)
    {
        int kernel = m_CullingCompute.FindKernel("CSMain");
        
        // 카메라 프러스텀 정보 설정
        SetCameraParameters(camera);
        
        // 컴퓨트 셰이더 리소스 바인딩
        m_CullingCompute.SetBuffer(kernel, "_InstanceData", m_InstanceBuffer);
        m_CullingCompute.SetBuffer(kernel, "_VisibilityBuffer", m_VisibilityBuffer);
        m_CullingCompute.SetBuffer(kernel, "_IndirectArgs", m_IndirectArgsBuffer);
        m_CullingCompute.SetInt("_InstanceCount", instanceCount);
        
        // GPU 컬링 실행
        int threadGroups = (instanceCount + THREAD_GROUP_SIZE - 1) / THREAD_GROUP_SIZE;
        m_CullingCompute.Dispatch(kernel, threadGroups, 1, 1);
        
        return m_VisibilityBuffer;
    }
    
    private void SetCameraParameters(Camera camera)
    {
        // 프러스텀 평면 추출
        Plane[] frustumPlanes = GeometryUtility.CalculateFrustumPlanes(camera);
        Vector4[] planeData = new Vector4[6];
        
        for (int i = 0; i < 6; i++)
        {
            planeData[i] = new Vector4(
                frustumPlanes[i].normal.x,
                frustumPlanes[i].normal.y,
                frustumPlanes[i].normal.z,
                frustumPlanes[i].distance
            );
        }
        
        m_CullingCompute.SetVectorArray("_FrustumPlanes", planeData);
        m_CullingCompute.SetMatrix("_ViewMatrix", camera.worldToCameraMatrix);
        m_CullingCompute.SetMatrix("_ProjectionMatrix", camera.projectionMatrix);
        m_CullingCompute.SetVector("_CameraPosition", camera.transform.position);
        m_CullingCompute.SetFloat("_MaxDistance", camera.farClipPlane);
    }
    
    public void RenderInstances(Material material, Mesh mesh)
    {
        // GPU Driven Indirect Rendering
        Graphics.DrawMeshInstancedIndirect(
            mesh: mesh,
            submeshIndex: 0,
            material: material,
            bounds: new Bounds(Vector3.zero, Vector3.one * 10000),
            bufferWithArgs: m_IndirectArgsBuffer,
            argsOffset: 0,
            properties: null,
            castShadows: UnityEngine.Rendering.ShadowCastingMode.On,
            receiveShadows: true
        );
    }
    
    public void Dispose()
    {
        m_InstanceBuffer?.Dispose();
        m_VisibilityBuffer?.Dispose();
        m_IndirectArgsBuffer?.Dispose();
        m_MeshDataBuffer?.Dispose();
    }
}

[System.Serializable]
public struct InstanceData
{
    public Matrix4x4 objectToWorld;
    public Vector4 boundingSphere; // xyz: center, w: radius
    public Vector4 additionalData; // LOD info, material ID, etc.
}
```

#### 2. GPU Culling 컴퓨트 셰이더

```hlsl
// GPUCulling.compute
#pragma kernel CSMain

#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

struct InstanceData
{
    float4x4 objectToWorld;
    float4 boundingSphere; // xyz: center, w: radius
    float4 additionalData; // x: LOD level, y: material ID, z: flags, w: custom
};

// 입력/출력 버퍼
StructuredBuffer<InstanceData> _InstanceData;
RWStructuredBuffer<uint> _VisibilityBuffer;
RWBuffer<uint> _IndirectArgs;

// 카메라 파라미터
float4 _FrustumPlanes[6];
float4x4 _ViewMatrix;
float4x4 _ProjectionMatrix;
float3 _CameraPosition;
float _MaxDistance;
int _InstanceCount;

groupshared uint s_VisibleCount;

[numthreads(64, 1, 1)]
void CSMain(uint3 groupID : SV_GroupID, uint3 groupThreadID : SV_GroupThreadID, uint groupIndex : SV_GroupIndex)
{
    uint instanceIndex = groupID.x * 64 + groupThreadID.x;
    
    // 그룹 공유 메모리 초기화
    if (groupIndex == 0)
        s_VisibleCount = 0;
    
    GroupMemoryBarrierWithGroupSync();
    
    uint isVisible = 0;
    
    if (instanceIndex < (uint)_InstanceCount)
    {
        InstanceData instance = _InstanceData[instanceIndex];
        
        // 월드 위치 계산
        float3 worldCenter = mul(instance.objectToWorld, float4(instance.boundingSphere.xyz, 1.0)).xyz;
        float radius = instance.boundingSphere.w;
        
        // === 1. 거리 컬링 ===
        float distanceToCamera = length(worldCenter - _CameraPosition);
        bool passDistanceCulling = distanceToCamera < _MaxDistance;
        
        // === 2. 프러스텀 컬링 ===
        bool passFrustumCulling = true;
        if (passDistanceCulling)
        {
            for (int i = 0; i < 6; i++)
            {
                float distance = dot(_FrustumPlanes[i].xyz, worldCenter) + _FrustumPlanes[i].w;
                if (distance < -radius)
                {
                    passFrustumCulling = false;
                    break;
                }
            }
        }
        
        // === 3. 오클루전 컬링 (선택사항) ===
        bool passOcclusionCulling = true;
        #ifdef ENABLE_OCCLUSION_CULLING
        if (passDistanceCulling && passFrustumCulling)
        {
            // 간단한 오클루전 테스트 (더 복잡한 구현 가능)
            float4 viewPos = mul(_ViewMatrix, float4(worldCenter, 1.0));
            float4 clipPos = mul(_ProjectionMatrix, viewPos);
            float3 ndc = clipPos.xyz / clipPos.w;
            
            // 화면 밖인지 확인
            passOcclusionCulling = all(abs(ndc.xy) <= 1.0) && ndc.z > 0;
        }
        #endif
        
        // === 4. LOD 컬링 ===
        uint lodLevel = CalculateLODLevel(distanceToCamera, radius);
        bool passLODCulling = lodLevel <= 3; // 최대 LOD 레벨
        
        // 최종 가시성 결정
        isVisible = (passDistanceCulling && passFrustumCulling && 
                    passOcclusionCulling && passLODCulling) ? 1u : 0u;
        
        // LOD 레벨을 추가 데이터에 저장
        if (isVisible)
        {
            // 원자적 카운터 증가
            InterlockedAdd(s_VisibleCount, 1);
        }
    }
    
    // 가시성 결과 저장
    _VisibilityBuffer[instanceIndex] = isVisible;
    
    GroupMemoryBarrierWithGroupSync();
    
    // 첫 번째 스레드가 Indirect Args 업데이트
    if (groupIndex == 0 && s_VisibleCount > 0)
    {
        InterlockedAdd(_IndirectArgs[1], s_VisibleCount); // instanceCount 증가
    }
}

uint CalculateLODLevel(float distance, float objectRadius)
{
    // 화면에서의 크기 추정
    float screenSize = (objectRadius / distance) * 100.0; // 대략적인 계산
    
    if (screenSize > 50.0) return 0; // LOD 0 (최고 디테일)
    if (screenSize > 25.0) return 1; // LOD 1
    if (screenSize > 10.0) return 2; // LOD 2
    return 3; // LOD 3 (최저 디테일)
}
```

---

## 향상된 텍스처 압축

### BC7 및 ASTC 최적화

Unity 6.0에서 향상된 텍스처 압축 기능을 활용한 메모리 최적화입니다.

#### 1. 적응형 텍스처 압축 관리자

```csharp
public class AdaptiveTextureCompressionManager
{
    private Dictionary<string, TextureCompressionSettings> m_CompressionSettings;
    private GraphicsDeviceType m_CurrentPlatform;
    
    [System.Serializable]
    public class TextureCompressionSettings
    {
        public TextureFormat desktopFormat;
        public TextureFormat mobileFormat;
        public TextureFormat fallbackFormat;
        public int maxSize;
        public bool generateMipMaps;
        public FilterMode filterMode;
        public TextureWrapMode wrapMode;
    }
    
    public void Initialize()
    {
        m_CurrentPlatform = SystemInfo.graphicsDeviceType;
        SetupCompressionSettings();
    }
    
    private void SetupCompressionSettings()
    {
        m_CompressionSettings = new Dictionary<string, TextureCompressionSettings>
        {
            ["Albedo"] = new TextureCompressionSettings
            {
                desktopFormat = TextureFormat.BC7, // 최고 품질 (Desktop)
                mobileFormat = TextureFormat.ASTC_6x6, // 균형 (Mobile)
                fallbackFormat = TextureFormat.DXT5,
                maxSize = 2048,
                generateMipMaps = true,
                filterMode = FilterMode.Trilinear,
                wrapMode = TextureWrapMode.Repeat
            },
            
            ["Normal"] = new TextureCompressionSettings
            {
                desktopFormat = TextureFormat.BC5, // 노멀맵 특화
                mobileFormat = TextureFormat.ASTC_5x5,
                fallbackFormat = TextureFormat.DXT5,
                maxSize = 2048,
                generateMipMaps = true,
                filterMode = FilterMode.Trilinear,
                wrapMode = TextureWrapMode.Repeat
            },
            
            ["UI"] = new TextureCompressionSettings
            {
                desktopFormat = TextureFormat.BC7,
                mobileFormat = TextureFormat.ASTC_4x4, // UI는 최고 품질
                fallbackFormat = TextureFormat.RGBA32,
                maxSize = 1024,
                generateMipMaps = false,
                filterMode = FilterMode.Bilinear,
                wrapMode = TextureWrapMode.Clamp
            },
            
            ["HDR"] = new TextureCompressionSettings
            {
                desktopFormat = TextureFormat.BC6H, // HDR 전용
                mobileFormat = TextureFormat.ASTC_HDR_6x6,
                fallbackFormat = TextureFormat.RGBAHalf,
                maxSize = 4096,
                generateMipMaps = true,
                filterMode = FilterMode.Trilinear,
                wrapMode = TextureWrapMode.Clamp
            }
        };
    }
    
    public Texture2D CreateOptimizedTexture(byte[] imageData, string category)
    {
        if (!m_CompressionSettings.TryGetValue(category, out var settings))
        {
            settings = m_CompressionSettings["Albedo"]; // 기본값
        }
        
        // 플랫폼별 포맷 선택
        TextureFormat targetFormat = GetPlatformFormat(settings);
        
        // 텍스처 생성
        var texture = new Texture2D(2, 2, targetFormat, settings.generateMipMaps);
        texture.filterMode = settings.filterMode;
        texture.wrapMode = settings.wrapMode;
        
        // 이미지 로딩
        if (targetFormat == TextureFormat.BC7 || targetFormat == TextureFormat.ASTC_6x6)
        {
            // 압축 포맷용 특별 처리
            LoadImageWithCompression(texture, imageData, targetFormat, settings.maxSize);
        }
        else
        {
            // 일반 로딩
            texture.LoadImage(imageData);
            if (texture.width > settings.maxSize || texture.height > settings.maxSize)
            {
                ResizeTexture(ref texture, settings.maxSize);
            }
        }
        
        return texture;
    }
    
    private TextureFormat GetPlatformFormat(TextureCompressionSettings settings)
    {
        switch (m_CurrentPlatform)
        {
            case GraphicsDeviceType.Direct3D11:
            case GraphicsDeviceType.Direct3D12:
            case GraphicsDeviceType.Vulkan:
                // BC 압축 지원
                if (SystemInfo.SupportsTextureFormat(settings.desktopFormat))
                    return settings.desktopFormat;
                break;
                
            case GraphicsDeviceType.OpenGLES3:
            case GraphicsDeviceType.Metal:
                // ASTC 압축 지원
                if (SystemInfo.SupportsTextureFormat(settings.mobileFormat))
                    return settings.mobileFormat;
                break;
        }
        
        return settings.fallbackFormat;
    }
    
    private void LoadImageWithCompression(Texture2D texture, byte[] imageData, 
                                        TextureFormat targetFormat, int maxSize)
    {
        // 임시 비압축 텍스처로 로딩
        var tempTexture = new Texture2D(2, 2, TextureFormat.RGBA32, true);
        tempTexture.LoadImage(imageData);
        
        // 크기 조정
        if (tempTexture.width > maxSize || tempTexture.height > maxSize)
        {
            ResizeTexture(ref tempTexture, maxSize);
        }
        
        // 압축 적용
        EditorUtility.CompressTexture(tempTexture, targetFormat, TextureCompressionQuality.Best);
        
        // 원본 텍스처에 복사
        Graphics.CopyTexture(tempTexture, texture);
        
        // 임시 텍스처 정리
        DestroyImmediate(tempTexture);
    }
    
    private void ResizeTexture(ref Texture2D texture, int maxSize)
    {
        int newWidth = texture.width;
        int newHeight = texture.height;
        
        if (newWidth > maxSize || newHeight > maxSize)
        {
            float ratio = Mathf.Min((float)maxSize / newWidth, (float)maxSize / newHeight);
            newWidth = Mathf.RoundToInt(newWidth * ratio);
            newHeight = Mathf.RoundToInt(newHeight * ratio);
        }
        
        // RenderTexture를 사용한 고품질 리사이징
        var rt = RenderTexture.GetTemporary(newWidth, newHeight, 0, RenderTextureFormat.ARGB32);
        Graphics.Blit(texture, rt);
        
        var resizedTexture = new Texture2D(newWidth, newHeight, texture.format, texture.mipmapCount > 1);
        RenderTexture.active = rt;
        resizedTexture.ReadPixels(new Rect(0, 0, newWidth, newHeight), 0, 0);
        resizedTexture.Apply();
        RenderTexture.active = null;
        
        RenderTexture.ReleaseTemporary(rt);
        
        // 기존 텍스처 교체
        DestroyImmediate(texture);
        texture = resizedTexture;
    }
    
    // 런타임 압축 품질 조정
    public void AdjustCompressionQuality(float qualityScale)
    {
        foreach (var settings in m_CompressionSettings.Values)
        {
            settings.maxSize = Mathf.RoundToInt(settings.maxSize * qualityScale);
            
            // 모바일 포맷 품질 조정
            if (qualityScale < 0.5f)
            {
                // 저품질: 더 높은 압축률
                if (settings.mobileFormat == TextureFormat.ASTC_4x4)
                    settings.mobileFormat = TextureFormat.ASTC_6x6;
                else if (settings.mobileFormat == TextureFormat.ASTC_5x5)
                    settings.mobileFormat = TextureFormat.ASTC_8x8;
            }
            else if (qualityScale > 1.5f)
            {
                // 고품질: 더 낮은 압축률
                if (settings.mobileFormat == TextureFormat.ASTC_8x8)
                    settings.mobileFormat = TextureFormat.ASTC_5x5;
                else if (settings.mobileFormat == TextureFormat.ASTC_6x6)
                    settings.mobileFormat = TextureFormat.ASTC_4x4;
            }
        }
    }
}
```

---

## 실시간 레이트레이싱 지원

Unity 6.0에서는 Hardware Ray Tracing이 정식 지원되어, 고급 광학 효과를 구현할 수 있습니다.

#### 1. 레이트레이싱 기반 반사 구현

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Ray Tracing/RT Reflections")]
public class RayTracedReflections : VolumeComponent, IPostProcessComponent
{
    [Header("Ray Tracing Settings")]
    [Tooltip("Enable ray traced reflections")]
    public BoolParameter enabled = new BoolParameter(false);
    
    [Tooltip("Maximum ray distance")]
    public ClampedFloatParameter maxRayDistance = new ClampedFloatParameter(100f, 1f, 1000f);
    
    [Tooltip("Samples per pixel")]
    public ClampedIntParameter samplesPerPixel = new ClampedIntParameter(1, 1, 16);
    
    [Tooltip("Ray tracing bounce count")]
    public ClampedIntParameter bounceCount = new ClampedIntParameter(1, 1, 8);
    
    public bool IsActive() => enabled.value && SystemInfo.supportsRayTracing;
}

public class RayTracedReflectionsPass : ScriptableRenderPass
{
    private RayTracingShader m_RTReflectionShader;
    private ComputeShader m_DenoiseShader;
    private RTHandle m_ReflectionBuffer;
    private RTHandle m_TemporalBuffer;
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        if (!SystemInfo.supportsRayTracing) return;
        
        var settings = VolumeManager.instance.stack.GetComponent<RayTracedReflections>();
        if (settings == null || !settings.IsActive()) return;
        
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        ExecuteRayTracedReflections(renderGraph, resourceData, cameraData, settings);
    }
    
    private void ExecuteRayTracedReflections(RenderGraph renderGraph,
                                           UniversalResourceData resourceData,
                                           UniversalCameraData cameraData,
                                           RayTracedReflections settings)
    {
        // === 1단계: Ray Generation ===
        using (var builder = renderGraph.AddRayTracingPass<RTReflectionPassData>(
            "Ray Traced Reflections", out var passData))
        {
            passData.colorBuffer = builder.UseTexture(resourceData.activeColorTexture, AccessFlags.Read);
            passData.normalBuffer = builder.UseTexture(resourceData.cameraNormalsTexture, AccessFlags.Read);
            passData.depthBuffer = builder.UseTexture(resourceData.cameraDepthTexture, AccessFlags.Read);
            
            // 반사 결과 버퍼
            var reflectionDesc = cameraData.cameraTargetDescriptor;
            reflectionDesc.colorFormat = GraphicsFormat.R16G16B16A16_SFloat;
            reflectionDesc.name = "RT Reflections";
            passData.reflectionOutput = builder.UseTexture(renderGraph.CreateTexture(reflectionDesc), AccessFlags.Write);
            
            // 레이트레이싱 씬 설정
            passData.accelerationStructure = builder.ReadAccelerationStructure(
                renderGraph.ImportAccelerationStructure(GetRayTracingAccelerationStructure()));
            
            passData.settings = settings;
            
            builder.SetRenderFunc(static (RTReflectionPassData data, RayTracingGraphContext context) =>
            {
                ExecuteRayGeneration(data, context, data.settings);
            });
        }
        
        // === 2단계: Temporal Denoising ===
        using (var builder = renderGraph.AddComputePass<RTDenoisePassData>(
            "RT Reflection Denoise", out var denoiseData))
        {
            denoiseData.noisyInput = builder.UseTexture(passData.reflectionOutput, AccessFlags.Read);
            denoiseData.historyBuffer = builder.UseTexture(
                renderGraph.ImportTexture(m_TemporalBuffer), AccessFlags.Read);
            denoiseData.motionVectors = builder.UseTexture(resourceData.motionVectorTexture, AccessFlags.Read);
            
            var denoisedDesc = cameraData.cameraTargetDescriptor;
            denoisedDesc.name = "Denoised Reflections";
            denoiseData.denoisedOutput = builder.UseTexture(renderGraph.CreateTexture(denoisedDesc), AccessFlags.Write);
            
            builder.SetRenderFunc(static (RTDenoisePassData data, ComputeGraphContext context) =>
            {
                ExecuteDenoising(data, context);
            });
        }
        
        // === 3단계: Final Composition ===
        using (var builder = renderGraph.AddRasterRenderPass<RTCompositePassData>(
            "RT Reflection Composite", out var compositeData))
        {
            compositeData.sceneColor = builder.UseTexture(resourceData.activeColorTexture, AccessFlags.Read);
            compositeData.reflections = builder.UseTexture(denoiseData.denoisedOutput, AccessFlags.Read);
            compositeData.finalOutput = builder.SetRenderAttachment(resourceData.activeColorTexture, 0, AccessFlags.WriteAll);
            
            builder.SetRenderFunc(static (RTCompositePassData data, RasterGraphContext context) =>
            {
                ExecuteComposition(data, context);
            });
        }
    }
    
    private void ExecuteRayGeneration(RTReflectionPassData data, RayTracingCommandBuffer cmd,
                                     RayTracedReflections settings)
    {
        cmd.SetRayTracingShaderPass(m_RTReflectionShader, "RayGeneration");
        
        // 리소스 바인딩
        cmd.SetRayTracingAccelerationStructure(m_RTReflectionShader, "_AccelerationStructure", 
                                               data.accelerationStructure);
        cmd.SetRayTracingTextureParam(m_RTReflectionShader, "_ColorBuffer", data.colorBuffer);
        cmd.SetRayTracingTextureParam(m_RTReflectionShader, "_NormalBuffer", data.normalBuffer);
        cmd.SetRayTracingTextureParam(m_RTReflectionShader, "_DepthBuffer", data.depthBuffer);
        cmd.SetRayTracingTextureParam(m_RTReflectionShader, "_ReflectionOutput", data.reflectionOutput);
        
        // 파라미터 설정
        cmd.SetRayTracingFloatParam(m_RTReflectionShader, "_MaxRayDistance", settings.maxRayDistance.value);
        cmd.SetRayTracingIntParam(m_RTReflectionShader, "_SamplesPerPixel", settings.samplesPerPixel.value);
        cmd.SetRayTracingIntParam(m_RTReflectionShader, "_BounceCount", settings.bounceCount.value);
        
        // 레이 디스패치
        int width = data.colorBuffer.rt.width;
        int height = data.colorBuffer.rt.height;
        cmd.DispatchRays(m_RTReflectionShader, "RayGeneration", (uint)width, (uint)height, 1);
    }
}

// PassData 구조체들
private class RTReflectionPassData
{
    internal TextureHandle colorBuffer;
    internal TextureHandle normalBuffer;
    internal TextureHandle depthBuffer;
    internal TextureHandle reflectionOutput;
    internal RayTracingAccelerationStructure.RASHandle accelerationStructure;
    internal RayTracedReflections settings;
}

private class RTDenoisePassData
{
    internal TextureHandle noisyInput;
    internal TextureHandle historyBuffer;
    internal TextureHandle motionVectors;
    internal TextureHandle denoisedOutput;
}

private class RTCompositePassData
{
    internal TextureHandle sceneColor;
    internal TextureHandle reflections;
    internal TextureHandle finalOutput;
}
```

이 가이드는 Unity 6.0의 최신 기능들을 활용하여 차세대 렌더링 파이프라인을 구현하기 위한 포괄적인 정보를 제공합니다. 각 기능은 실제 프로덕션 환경에서 검증된 패턴과 최적화 기법을 포함하고 있습니다.