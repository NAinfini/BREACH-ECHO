# Unity 6.0 렌더링 파이프라인 코어 개발 가이드

## 개요

Unity 6.0의 렌더링 파이프라인 코어 패키지(`com.unity.render-pipelines.core`)는 Scriptable Render Pipeline(SRP) 시스템의 기반을 제공합니다. 이 가이드는 Volume System, RenderGraph 인프라, 그리고 셰이더 라이브러리를 활용한 고급 렌더링 기법 구현을 다룹니다.

## 목차

1. [Volume System 마스터링](#volume-system-마스터링)
2. [RenderGraph 기본 인프라](#rendergraph-기본-인프라)
3. [CommandBuffer 유틸리티 활용](#commandbuffer-유틸리티-활용)
4. [셰이더 라이브러리 기반](#셰이더-라이브러리-기반)
5. [고급 최적화 기법](#고급-최적화-기법)
6. [플랫폼별 구현 전략](#플랫폼별-구현-전략)
7. [실전 구현 예제](#실전-구현-예제)
8. [성능 프로파일링](#성능-프로파일링)
9. [문제해결 및 디버깅](#문제해결-및-디버깅)

---

## Volume System 마스터링

### VolumeComponent 고급 구현

#### 1. 완전한 VolumeComponent 구조

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Advanced/Complex Effect")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
[URPHelpURL("post-processing-complex-effect")]
public sealed class ComplexEffect : VolumeComponent, IPostProcessComponent
{
    [Header("Primary Parameters")]
    [Tooltip("Main effect intensity")]
    public ClampedFloatParameter intensity = new ClampedFloatParameter(0f, 0f, 2f);
    
    [Tooltip("Effect quality preset")]
    public QualityPresetParameter quality = new QualityPresetParameter(QualityPreset.Medium);
    
    [Header("Color Manipulation")]
    [Tooltip("Primary tint color")]
    public ColorParameter primaryTint = new ColorParameter(Color.white, true, false, true);
    
    [Tooltip("Secondary tint color")]
    public ColorParameter secondaryTint = new ColorParameter(Color.white, true, false, true);
    
    [Tooltip("Blend factor between tints")]
    [ShowAdditionalProperty]
    public ClampedFloatParameter tintBlend = new ClampedFloatParameter(0.5f, 0f, 1f);
    
    [Header("Spatial Parameters")]
    [Tooltip("Effect center point")]
    public Vector2Parameter center = new Vector2Parameter(new Vector2(0.5f, 0.5f));
    
    [Tooltip("Effect radius")]
    public MinFloatParameter radius = new MinFloatParameter(1f, 0f);
    
    [Tooltip("Radius falloff curve")]
    public AnimationCurveParameter falloffCurve = new AnimationCurveParameter(
        AnimationCurve.EaseInOut(0f, 1f, 1f, 0f), false);
    
    [Header("Advanced Controls")]
    [Tooltip("Custom noise texture")]
    public TextureParameter noiseTexture = new TextureParameter(null);
    
    [Tooltip("Temporal settings")]
    public TemporalSettingsParameter temporal = new TemporalSettingsParameter(new TemporalSettings());
    
    [Header("Performance")]
    [Tooltip("Use half precision when possible")]
    public BoolParameter useHalfPrecision = new BoolParameter(true);
    
    [Tooltip("Enable platform-specific optimizations")]
    public BoolParameter enableOptimizations = new BoolParameter(true);
    
    // 활성화 조건 (복합 조건)
    public bool IsActive()
    {
        return intensity.value > 0f && 
               quality.value != QualityPreset.Off &&
               (primaryTint.value.a > 0f || secondaryTint.value.a > 0f);
    }
    
    
    // 커스텀 오버라이드 로직
    public override void Override(VolumeComponent state, float interpFactor)
    {
        base.Override(state, interpFactor);
        
        var complexState = (ComplexEffect)state;
        
        // 특별한 블렌딩 로직 (예: 색상 공간 변환 후 블렌딩)
        if (primaryTint.overrideState && secondaryTint.overrideState)
        {
            // HSV 공간에서 색상 블렌딩
            Color.RGBToHSV(complexState.primaryTint.value, out float h1, out float s1, out float v1);
            Color.RGBToHSV(primaryTint.value, out float h2, out float s2, out float v2);
            
            float blendedH = Mathf.LerpAngle(h1 * 360f, h2 * 360f, interpFactor) / 360f;
            float blendedS = Mathf.Lerp(s1, s2, interpFactor);
            float blendedV = Mathf.Lerp(v1, v2, interpFactor);
            
            complexState.primaryTint.value = Color.HSVToRGB(blendedH, blendedS, blendedV);
        }
    }
}
```

#### 2. 커스텀 파라미터 타입 구현

```csharp
// 품질 프리셋 파라미터
[Serializable]
public sealed class QualityPresetParameter : VolumeParameter<QualityPreset>
{
    public QualityPresetParameter(QualityPreset value, bool overrideState = false) 
        : base(value, overrideState) { }
    
    // 커스텀 보간 (스냅 방식)
    public override void Interp(QualityPreset from, QualityPreset to, float t)
    {
        m_Value = t < 0.5f ? from : to;
    }
}

public enum QualityPreset
{
    Off = 0,
    Low = 1,
    Medium = 2,
    High = 3,
    Ultra = 4
}

// 복합 구조체 파라미터
[Serializable]
public struct TemporalSettings
{
    public bool enableTAA;
    public float temporalBlend;
    public int historyFrames;
    
    public static TemporalSettings Default => new TemporalSettings
    {
        enableTAA = false,
        temporalBlend = 0.1f,
        historyFrames = 8
    };
}

[Serializable]
public sealed class TemporalSettingsParameter : VolumeParameter<TemporalSettings>
{
    public TemporalSettingsParameter(TemporalSettings value, bool overrideState = false) 
        : base(value, overrideState) { }
    
    public override void Interp(TemporalSettings from, TemporalSettings to, float t)
    {
        // 구조체의 각 필드를 개별적으로 보간
        m_Value = new TemporalSettings
        {
            enableTAA = t > 0.5f ? to.enableTAA : from.enableTAA,
            temporalBlend = Mathf.Lerp(from.temporalBlend, to.temporalBlend, t),
            historyFrames = t > 0.5f ? to.historyFrames : from.historyFrames
        };
    }
}

// 커스텀 보간 파라미터 (예: 지수 보간)
[Serializable]
public sealed class ExponentialFloatParameter : VolumeParameter<float>
{
    public float exponent = 2f;
    
    public ExponentialFloatParameter(float value, float exp = 2f, bool overrideState = false) 
        : base(value, overrideState) 
    {
        exponent = exp;
    }
    
    public override void Interp(float from, float to, float t)
    {
        // 지수 곡선 보간
        float curved = Mathf.Pow(t, exponent);
        m_Value = Mathf.Lerp(from, to, curved);
    }
}
```

### Volume Manager 고급 활용

#### 1. 커스텀 Volume Manager 확장

```csharp
public static class VolumeManagerExtensions
{
    // 특정 카메라를 위한 Volume Stack 생성
    public static VolumeStack CreateStackForCamera(Camera camera, LayerMask layerMask)
    {
        var stack = new VolumeStack();
        var volumes = VolumeManager.instance.volumes;
        
        // 카메라 위치와 레이어마스크를 기반으로 영향받는 볼륨 수집
        var relevantVolumes = volumes
            .Where(v => (layerMask & (1 << v.gameObject.layer)) != 0)
            .Where(v => IsVolumeAffectingCamera(v, camera))
            .OrderBy(v => v.priority)
            .ToList();
        
        // Volume Stack 업데이트
        VolumeManager.instance.Update(stack, camera.transform, layerMask);
        
        return stack;
    }
    
    private static bool IsVolumeAffectingCamera(Volume volume, Camera camera)
    {
        if (!volume.enabled || volume.weight <= 0f)
            return false;
            
        if (volume.isGlobal)
            return true;
            
        // Collider 기반 볼륨 체크
        var collider = volume.GetComponent<Collider>();
        return collider != null && collider.bounds.Contains(camera.transform.position);
    }
    
    // Volume 파라미터 디버깅 정보
    public static VolumeDebugInfo GetDebugInfo<T>(this VolumeStack stack) where T : VolumeComponent
    {
        var component = stack.GetComponent<T>();
        if (component == null)
            return null;
            
        return new VolumeDebugInfo
        {
            componentType = typeof(T),
            activeParameters = component.parameters
                .Where(p => p.overrideState)
                .Select(p => new ParameterDebugInfo
                {
                    name = p.GetType().Name,
                    value = p.GetValue<object>()?.ToString() ?? "null",
                    overrideState = p.overrideState
                })
                .ToList()
        };
    }
}

[Serializable]
public class VolumeDebugInfo
{
    public Type componentType;
    public List<ParameterDebugInfo> activeParameters;
}

[Serializable]
public class ParameterDebugInfo
{
    public string name;
    public string value;
    public bool overrideState;
}
```

#### 2. 런타임 Volume 조작

```csharp
public class RuntimeVolumeController : MonoBehaviour
{
    [SerializeField] private VolumeProfile m_BaseProfile;
    [SerializeField] private Volume m_RuntimeVolume;
    
    private ComplexEffect m_ComplexEffect;
    
    void Start()
    {
        // 런타임에 Volume 설정
        SetupRuntimeVolume();
    }
    
    void SetupRuntimeVolume()
    {
        if (m_RuntimeVolume == null)
        {
            // 동적으로 Volume 생성
            var volumeGO = new GameObject("Runtime Volume");
            m_RuntimeVolume = volumeGO.AddComponent<Volume>();
            m_RuntimeVolume.isGlobal = true;
            m_RuntimeVolume.priority = 100;
        }
        
        // VolumeProfile 생성 및 설정
        if (m_RuntimeVolume.profile == null)
        {
            m_RuntimeVolume.profile = ScriptableObject.CreateInstance<VolumeProfile>();
        }
        
        // 컴포넌트 추가 및 설정
        if (!m_RuntimeVolume.profile.TryGet<ComplexEffect>(out m_ComplexEffect))
        {
            m_ComplexEffect = m_RuntimeVolume.profile.Add<ComplexEffect>();
        }
        
        // 초기값 설정
        m_ComplexEffect.intensity.overrideState = true;
        m_ComplexEffect.intensity.value = 0.5f;
        m_ComplexEffect.quality.overrideState = true;
        m_ComplexEffect.quality.value = QualityPreset.High;
    }
    
    // 애니메이션 가능한 프로퍼티들
    public void SetIntensity(float intensity)
    {
        if (m_ComplexEffect != null)
        {
            m_ComplexEffect.intensity.value = intensity;
        }
    }
    
    public void SetCenter(Vector2 center)
    {
        if (m_ComplexEffect != null)
        {
            m_ComplexEffect.center.overrideState = true;
            m_ComplexEffect.center.value = center;
        }
    }
    
    // 부드러운 전환을 위한 코루틴
    public Coroutine TransitionToProfile(VolumeProfile targetProfile, float duration)
    {
        return StartCoroutine(TransitionCoroutine(targetProfile, duration));
    }
    
    private IEnumerator TransitionCoroutine(VolumeProfile targetProfile, float duration)
    {
        var originalWeight = m_RuntimeVolume.weight;
        var tempVolume = CreateTemporaryVolume(targetProfile);
        
        float elapsed = 0f;
        while (elapsed < duration)
        {
            elapsed += Time.deltaTime;
            float t = elapsed / duration;
            
            // 부드러운 곡선 적용
            t = Mathf.SmoothStep(0f, 1f, t);
            
            tempVolume.weight = t;
            m_RuntimeVolume.weight = originalWeight * (1f - t);
            
            yield return null;
        }
        
        // 전환 완료
        CopyProfile(targetProfile, m_RuntimeVolume.profile);
        m_RuntimeVolume.weight = originalWeight;
        DestroyTemporaryVolume(tempVolume);
    }
    
    private Volume CreateTemporaryVolume(VolumeProfile profile)
    {
        var tempGO = new GameObject("Temp Volume");
        var tempVolume = tempGO.AddComponent<Volume>();
        tempVolume.profile = profile;
        tempVolume.isGlobal = true;
        tempVolume.priority = m_RuntimeVolume.priority + 1;
        tempVolume.weight = 0f;
        return tempVolume;
    }
    
    private void CopyProfile(VolumeProfile source, VolumeProfile destination)
    {
        // VolumeProfile의 모든 컴포넌트 복사
        destination.components.Clear();
        foreach (var component in source.components)
        {
            var copy = Instantiate(component);
            destination.components.Add(copy);
        }
    }
    
    private void DestroyTemporaryVolume(Volume volume)
    {
        if (volume != null)
        {
            DestroyImmediate(volume.gameObject);
        }
    }
}
```

---

## RenderGraph 기본 인프라

### 고급 TextureHandle 관리

#### 1. 커스텀 텍스처 풀링 시스템

```csharp
public class ManagedTexturePool
{
    private struct TextureKey
    {
        public int width, height;
        public GraphicsFormat format;
        public TextureDimension dimension;
        public int msaaSamples;
        
        public override int GetHashCode()
        {
            return HashCode.Combine(width, height, (int)format, (int)dimension, msaaSamples);
        }
    }
    
    private readonly Dictionary<TextureKey, Queue<RTHandle>> m_Pool = new();
    private readonly HashSet<RTHandle> m_InUse = new();
    
    public RTHandle GetTemporary(TextureDesc desc)
    {
        var key = new TextureKey
        {
            width = desc.width,
            height = desc.height,
            format = desc.colorFormat,
            dimension = desc.dimension,
            msaaSamples = (int)desc.msaaSamples
        };
        
        if (m_Pool.TryGetValue(key, out var queue) && queue.Count > 0)
        {
            var texture = queue.Dequeue();
            m_InUse.Add(texture);
            return texture;
        }
        
        // 새 텍스처 생성
        var newTexture = RTHandles.Alloc(desc.width, desc.height, 
            colorFormat: desc.colorFormat,
            dimension: desc.dimension,
            msaaSamples: desc.msaaSamples,
            name: $"Pooled_{key.GetHashCode():X8}");
            
        m_InUse.Add(newTexture);
        return newTexture;
    }
    
    public void ReleaseTemporary(RTHandle texture)
    {
        if (texture == null || !m_InUse.Remove(texture))
            return;
            
        var key = GetKeyFromTexture(texture);
        if (!m_Pool.TryGetValue(key, out var queue))
        {
            queue = new Queue<RTHandle>();
            m_Pool[key] = queue;
        }
        
        queue.Enqueue(texture);
        
        // 풀 크기 제한
        if (queue.Count > 10) // 최대 10개까지 캐시
        {
            var excess = queue.Dequeue();
            RTHandles.Release(excess);
        }
    }
    
    private TextureKey GetKeyFromTexture(RTHandle texture)
    {
        return new TextureKey
        {
            width = texture.rt.width,
            height = texture.rt.height,
            format = texture.rt.graphicsFormat,
            dimension = texture.rt.dimension,
            msaaSamples = texture.rt.antiAliasing
        };
    }
    
    public void ClearPool()
    {
        foreach (var queue in m_Pool.Values)
        {
            while (queue.Count > 0)
            {
                RTHandles.Release(queue.Dequeue());
            }
        }
        m_Pool.Clear();
        
        foreach (var texture in m_InUse)
        {
            RTHandles.Release(texture);
        }
        m_InUse.Clear();
    }
}
```

#### 2. 고급 RenderGraph 패턴

```csharp
public class MultiPassRenderGraphExecutor
{
    private struct PassInfo
    {
        public string name;
        public System.Action<RenderGraph, TextureHandle, TextureHandle> executeFunc;
        public TextureDesc? customOutputDesc;
    }
    
    private readonly List<PassInfo> m_Passes = new();
    private readonly ManagedTexturePool m_TexturePool = new();
    
    public MultiPassRenderGraphExecutor AddPass(string name, 
        System.Action<RenderGraph, TextureHandle, TextureHandle> executeFunc,
        TextureDesc? customOutputDesc = null)
    {
        m_Passes.Add(new PassInfo
        {
            name = name,
            executeFunc = executeFunc,
            customOutputDesc = customOutputDesc
        });
        return this;
    }
    
    public TextureHandle Execute(RenderGraph renderGraph, TextureHandle input, TextureDesc baseDesc)
    {
        var currentInput = input;
        TextureHandle finalOutput = input;
        
        for (int i = 0; i < m_Passes.Count; i++)
        {
            var pass = m_Passes[i];
            var isLastPass = (i == m_Passes.Count - 1);
            
            // 출력 텍스처 결정
            TextureDesc outputDesc = pass.customOutputDesc ?? baseDesc;
            outputDesc.name = $"{pass.name}_Output_{i}";
            
            var output = renderGraph.CreateTexture(outputDesc);
            
            // 패스 실행
            pass.executeFunc(renderGraph, currentInput, output);
            
            // 다음 패스를 위해 입력 업데이트
            currentInput = output;
            
            if (isLastPass)
            {
                finalOutput = output;
            }
        }
        
        return finalOutput;
    }
    
    // 빌더 패턴 메서드들
    public MultiPassRenderGraphExecutor AddBlurPass(Material blurMaterial, int iterations)
    {
        for (int i = 0; i < iterations; i++)
        {
            AddPass($"Blur_Iteration_{i}", (rg, input, output) =>
            {
                ExecuteBlurPass(rg, input, output, blurMaterial, i);
            });
        }
        return this;
    }
    
    public MultiPassRenderGraphExecutor AddDownsamplePass(int factor = 2)
    {
        AddPass("Downsample", (rg, input, output) =>
        {
            ExecuteDownsamplePass(rg, input, output, factor);
        }, new TextureDesc
        {
            width = baseDesc.width / factor,
            height = baseDesc.height / factor,
            colorFormat = baseDesc.colorFormat
        });
        return this;
    }
    
    public MultiPassRenderGraphExecutor AddUpsamplePass()
    {
        AddPass("Upsample", (rg, input, output) =>
        {
            ExecuteUpsamplePass(rg, input, output);
        });
        return this;
    }
    
    private void ExecuteBlurPass(RenderGraph rg, TextureHandle input, TextureHandle output, 
                               Material blurMaterial, int iteration)
    {
        using (var builder = rg.AddRasterRenderPass<BlurPassData>($"Blur_{iteration}", out var passData))
        {
            passData.source = builder.UseTexture(input, AccessFlags.Read);
            passData.destination = builder.SetRenderAttachment(output, 0, AccessFlags.WriteAll);
            passData.material = blurMaterial;
            passData.blurRadius = 1f + iteration * 0.5f; // 점진적 블러 확장
            
            builder.SetRenderFunc(static (BlurPassData data, RasterGraphContext context) =>
            {
                data.material.SetFloat("_BlurRadius", data.blurRadius);
                Blitter.BlitCameraTexture(context.cmd, data.source, data.destination, data.material, 0);
            });
        }
    }
    
    private void ExecuteDownsamplePass(RenderGraph rg, TextureHandle input, TextureHandle output, int factor)
    {
        using (var builder = rg.AddRasterRenderPass<DownsamplePassData>("Downsample", out var passData))
        {
            passData.source = builder.UseTexture(input, AccessFlags.Read);
            passData.destination = builder.SetRenderAttachment(output, 0, AccessFlags.WriteAll);
            passData.downsampleFactor = factor;
            
            builder.SetRenderFunc(static (DownsamplePassData data, RasterGraphContext context) =>
            {
                // 고품질 다운샘플링 (13-tap)
                context.cmd.SetGlobalFloat("_DownsampleFactor", data.downsampleFactor);
                Blitter.BlitCameraTexture(context.cmd, data.source, data.destination, 
                    GetDownsampleMaterial(), 0);
            });
        }
    }
    
    private void ExecuteUpsamplePass(RenderGraph rg, TextureHandle input, TextureHandle output)
    {
        using (var builder = rg.AddRasterRenderPass<UpsamplePassData>("Upsample", out var passData))
        {
            passData.source = builder.UseTexture(input, AccessFlags.Read);
            passData.destination = builder.SetRenderAttachment(output, 0, AccessFlags.WriteAll);
            
            builder.SetRenderFunc(static (UpsamplePassData data, RasterGraphContext context) =>
            {
                // 바이큐빅 업샘플링
                Blitter.BlitCameraTexture(context.cmd, data.source, data.destination, 
                    GetUpsampleMaterial(), 0);
            });
        }
    }
}

// PassData 클래스들
private class BlurPassData
{
    internal TextureHandle source;
    internal TextureHandle destination;
    internal Material material;
    internal float blurRadius;
}

private class DownsamplePassData
{
    internal TextureHandle source;
    internal TextureHandle destination;
    internal int downsampleFactor;
}

private class UpsamplePassData
{
    internal TextureHandle source;
    internal TextureHandle destination;
}
```

### BufferHandle과 Compute Shader 통합

#### 1. Compute Shader 기반 RenderGraph 패스

```csharp
public class ComputeBasedPostProcess
{
    private ComputeShader m_ComputeShader;
    private int m_KernelIndex;
    private readonly int m_ThreadGroupSize = 8;
    
    public ComputeBasedPostProcess(ComputeShader computeShader, string kernelName)
    {
        m_ComputeShader = computeShader;
        m_KernelIndex = computeShader.FindKernel(kernelName);
    }
    
    public void ExecuteComputePass(RenderGraph renderGraph, TextureHandle input, TextureHandle output,
                                  ComputeParameters parameters)
    {
        using (var builder = renderGraph.AddComputePass<ComputePassData>("Compute Post Process", out var passData))
        {
            // 텍스처 리소스 설정
            passData.inputTexture = builder.UseTexture(input, AccessFlags.Read);
            passData.outputTexture = builder.UseTexture(output, AccessFlags.Write);
            
            // 파라미터 버퍼 생성 및 설정
            var parameterBufferDesc = new BufferDesc
            {
                count = 1,
                stride = Marshal.SizeOf<ComputeParameters>(),
                target = GraphicsBuffer.Target.Constant
            };
            
            passData.parameterBuffer = builder.CreateTransientBuffer(parameterBufferDesc);
            passData.parameters = parameters;
            passData.computeShader = m_ComputeShader;
            passData.kernelIndex = m_KernelIndex;
            
            // 스레드 그룹 계산
            var inputDesc = renderGraph.GetTextureDesc(input);
            passData.threadGroupsX = (inputDesc.width + m_ThreadGroupSize - 1) / m_ThreadGroupSize;
            passData.threadGroupsY = (inputDesc.height + m_ThreadGroupSize - 1) / m_ThreadGroupSize;
            
            builder.SetRenderFunc(static (ComputePassData data, ComputeGraphContext context) =>
            {
                // 파라미터 버퍼 업데이트
                var bufferArray = new ComputeParameters[] { data.parameters };
                context.cmd.SetBufferData(data.parameterBuffer, bufferArray);
                
                // Compute Shader 설정
                context.cmd.SetComputeTextureParam(data.computeShader, data.kernelIndex, 
                    "_InputTexture", data.inputTexture);
                context.cmd.SetComputeTextureParam(data.computeShader, data.kernelIndex, 
                    "_OutputTexture", data.outputTexture);
                context.cmd.SetComputeBufferParam(data.computeShader, data.kernelIndex, 
                    "_Parameters", data.parameterBuffer);
                
                // Dispatch
                context.cmd.DispatchCompute(data.computeShader, data.kernelIndex, 
                    data.threadGroupsX, data.threadGroupsY, 1);
            });
        }
    }
}

private class ComputePassData
{
    internal TextureHandle inputTexture;
    internal TextureHandle outputTexture;
    internal BufferHandle parameterBuffer;
    internal ComputeParameters parameters;
    internal ComputeShader computeShader;
    internal int kernelIndex;
    internal int threadGroupsX;
    internal int threadGroupsY;
}

[StructLayout(LayoutKind.Sequential)]
public struct ComputeParameters
{
    public float intensity;
    public Vector2 center;
    public float radius;
    public float time;
    // ... 추가 파라미터들
}
```

---

## CommandBuffer 유틸리티 활용

### CoreUtils 고급 활용

#### 1. 커스텀 Blitter 구현

```csharp
public static class AdvancedBlitter
{
    private static readonly int s_BlitScaleBias = Shader.PropertyToID("_BlitScaleBias");
    private static readonly int s_BlitMipLevel = Shader.PropertyToID("_BlitMipLevel");
    private static readonly int s_BlitTexture = Shader.PropertyToID("_BlitTexture");
    
    // 고급 블릿 (스케일, 바이어스, MIP 레벨 제어)
    public static void BlitTextureWithParams(CommandBuffer cmd, 
        RTHandle source, RTHandle destination, 
        Material material, int pass,
        Vector4 scaleBias, int mipLevel = 0)
    {
        material.SetVector(s_BlitScaleBias, scaleBias);
        material.SetFloat(s_BlitMipLevel, mipLevel);
        material.SetTexture(s_BlitTexture, source);
        
        CoreUtils.SetRenderTarget(cmd, destination);
        CoreUtils.DrawFullScreen(cmd, material, shaderPassId: pass);
    }
    
    // 다중 타겟 블릿
    public static void BlitToMultipleTargets(CommandBuffer cmd,
        RTHandle source, RTHandle[] destinations,
        Material material, int pass)
    {
        var colorBuffers = new RenderTargetIdentifier[destinations.Length];
        for (int i = 0; i < destinations.Length; i++)
        {
            colorBuffers[i] = destinations[i];
        }
        
        cmd.SetRenderTarget(colorBuffers, destinations[0]); // 첫 번째를 깊이 버퍼로 사용
        material.SetTexture(s_BlitTexture, source);
        CoreUtils.DrawFullScreen(cmd, material, shaderPassId: pass);
    }
    
    // 영역별 블릿 (ROI: Region of Interest)
    public static void BlitRegion(CommandBuffer cmd,
        RTHandle source, RTHandle destination,
        Material material, int pass,
        Rect sourceRect, Rect destRect)
    {
        // 정규화된 좌표계로 변환
        var sourceUV = new Vector4(
            sourceRect.x / source.rt.width,
            sourceRect.y / source.rt.height,
            sourceRect.width / source.rt.width,
            sourceRect.height / source.rt.height
        );
        
        var destViewport = new Vector4(
            destRect.x, destRect.y,
            destRect.width, destRect.height
        );
        
        material.SetVector("_SourceUV", sourceUV);
        material.SetTexture(s_BlitTexture, source);
        
        cmd.SetRenderTarget(destination);
        cmd.SetViewport(new Rect(destViewport.x, destViewport.y, destViewport.z, destViewport.w));
        CoreUtils.DrawFullScreen(cmd, material, shaderPassId: pass);
    }
    
    // GPU 인스턴싱을 사용한 배치 블릿
    public static void BlitInstanced(CommandBuffer cmd,
        RTHandle source, RTHandle destination,
        Material material, int pass,
        Matrix4x4[] transformMatrices, int instanceCount)
    {
        material.SetTexture(s_BlitTexture, source);
        
        // 인스턴스 데이터 설정
        var transformBuffer = new ComputeBuffer(instanceCount, Marshal.SizeOf<Matrix4x4>());
        transformBuffer.SetData(transformMatrices);
        material.SetBuffer("_TransformMatrices", transformBuffer);
        
        cmd.SetRenderTarget(destination);
        cmd.DrawMeshInstanced(RenderingUtils.fullscreenMesh, 0, material, pass,
            transformMatrices, instanceCount);
        
        transformBuffer.Release();
    }
}
```

#### 2. 고급 프로파일링 시스템

```csharp
public class AdvancedProfiler : IDisposable
{
    private struct ProfilerScope
    {
        public ProfilingSampler sampler;
        public CommandBuffer cmd;
        public float startTime;
    }
    
    private readonly Stack<ProfilerScope> m_ScopeStack = new();
    private readonly Dictionary<string, ProfileStats> m_Stats = new();
    private readonly Queue<float> m_FrameTimes = new();
    private const int MaxFrameHistory = 60;
    
    public class ProfileStats
    {
        public float totalTime;
        public float minTime = float.MaxValue;
        public float maxTime;
        public int callCount;
        public float averageTime => callCount > 0 ? totalTime / callCount : 0f;
    }
    
    public void BeginSample(CommandBuffer cmd, string sampleName)
    {
        var sampler = ProfilingSampler.Get(URPProfileId.RG_CustomSampler);
        sampler.Begin(cmd);
        
        m_ScopeStack.Push(new ProfilerScope
        {
            sampler = sampler,
            cmd = cmd,
            startTime = Time.realtimeSinceStartup
        });
        
        // GPU 타이머 시작
        cmd.BeginSample(sampleName);
    }
    
    public void EndSample(string sampleName)
    {
        if (m_ScopeStack.Count == 0)
            return;
            
        var scope = m_ScopeStack.Pop();
        var duration = Time.realtimeSinceStartup - scope.startTime;
        
        // GPU 타이머 종료
        scope.cmd.EndSample(sampleName);
        scope.sampler.End(scope.cmd);
        
        // 통계 업데이트
        UpdateStats(sampleName, duration);
    }
    
    private void UpdateStats(string sampleName, float duration)
    {
        if (!m_Stats.TryGetValue(sampleName, out var stats))
        {
            stats = new ProfileStats();
            m_Stats[sampleName] = stats;
        }
        
        stats.totalTime += duration;
        stats.callCount++;
        stats.minTime = Mathf.Min(stats.minTime, duration);
        stats.maxTime = Mathf.Max(stats.maxTime, duration);
    }
    
    public void RecordFrameTime(float frameTime)
    {
        m_FrameTimes.Enqueue(frameTime);
        if (m_FrameTimes.Count > MaxFrameHistory)
            m_FrameTimes.Dequeue();
    }
    
    public ProfilerReport GenerateReport()
    {
        var report = new ProfilerReport();
        report.samples = new List<ProfilerSampleReport>();
        
        foreach (var kvp in m_Stats)
        {
            report.samples.Add(new ProfilerSampleReport
            {
                name = kvp.Key,
                totalTime = kvp.Value.totalTime,
                averageTime = kvp.Value.averageTime,
                minTime = kvp.Value.minTime,
                maxTime = kvp.Value.maxTime,
                callCount = kvp.Value.callCount
            });
        }
        
        // 프레임 시간 통계
        if (m_FrameTimes.Count > 0)
        {
            report.averageFrameTime = m_FrameTimes.Average();
            report.minFrameTime = m_FrameTimes.Min();
            report.maxFrameTime = m_FrameTimes.Max();
            report.averageFPS = 1000f / report.averageFrameTime;
        }
        
        return report;
    }
    
    public void ResetStats()
    {
        m_Stats.Clear();
        m_FrameTimes.Clear();
    }
    
    public void Dispose()
    {
        while (m_ScopeStack.Count > 0)
        {
            var scope = m_ScopeStack.Pop();
            scope.sampler.End(scope.cmd);
        }
        ResetStats();
    }
}

[Serializable]
public class ProfilerReport
{
    public List<ProfilerSampleReport> samples;
    public float averageFrameTime;
    public float minFrameTime;
    public float maxFrameTime;
    public float averageFPS;
}

[Serializable]
public class ProfilerSampleReport
{
    public string name;
    public float totalTime;
    public float averageTime;
    public float minTime;
    public float maxTime;
    public int callCount;
}
```

---

## 셰이더 라이브러리 기반

### Core.hlsl 고급 활용

#### 1. 플랫폼별 최적화 매크로

```hlsl
// AdvancedCommon.hlsl
#ifndef ADVANCED_COMMON_INCLUDED
#define ADVANCED_COMMON_INCLUDED

#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl"
#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Macros.hlsl"

// 확장된 수학 상수들
#define GOLDEN_RATIO    1.61803398874989484820
#define SQRT_2          1.41421356237309504880
#define SQRT_3          1.73205080756887729352
#define E               2.71828182845904523536

// 고급 interpolation 함수들
#define DECLARE_SMOOTH_INTERPOLATORS(TYPE) \
    TYPE smoothstep5(TYPE x) { return x * x * x * (x * (x * 6.0 - 15.0) + 10.0); } \
    TYPE smoothstep7(TYPE x) { return x * x * x * x * (x * (x * (x * -20.0 + 70.0) - 84.0) + 35.0); }

DECLARE_SMOOTH_INTERPOLATORS(float)
DECLARE_SMOOTH_INTERPOLATORS(float2)
DECLARE_SMOOTH_INTERPOLATORS(float3)
DECLARE_SMOOTH_INTERPOLATORS(float4)

// 색상 공간 변환 함수들
float3 RGBToHSV(float3 c)
{
    float4 K = float4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    float4 p = lerp(float4(c.bg, K.wz), float4(c.gb, K.xy), step(c.b, c.g));
    float4 q = lerp(float4(p.xyw, c.r), float4(c.r, p.yzx), step(p.x, c.r));

    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return float3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

float3 HSVToRGB(float3 c)
{
    float4 K = float4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    float3 p = abs(frac(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * lerp(K.xxx, saturate(p - K.xxx), c.y);
}

// 고급 노이즈 함수들
float hash21(float2 p)
{
    p = frac(p * float2(234.34, 435.345));
    p += dot(p, p + 34.23);
    return frac(p.x * p.y);
}

float2 hash22(float2 p)
{
    p = frac(p * float2(234.34, 435.345));
    p += dot(p, p + 34.23);
    return frac(float2(p.x * p.y, (p.x + p.y) * p.x));
}

float voronoi(float2 uv, float scale)
{
    uv *= scale;
    float2 i = floor(uv);
    float2 f = frac(uv);
    
    float minDist = 1.0;
    for (int y = -1; y <= 1; y++)
    {
        for (int x = -1; x <= 1; x++)
        {
            float2 neighbor = float2(x, y);
            float2 point = hash22(i + neighbor);
            float2 diff = neighbor + point - f;
            float dist = length(diff);
            minDist = min(minDist, dist);
        }
    }
    
    return minDist;
}

// GPU Gems의 고급 필터링
float4 BicubicSample(TEXTURE2D_PARAM(tex, sampler_tex), float2 uv, float4 texelSize)
{
    float2 coord = uv * texelSize.zw - 0.5;
    float2 icoord = floor(coord);
    float2 fcoord = frac(coord);
    
    // 큐빅 가중치 계산
    float2 w0, w1, w2, w3;
    cubic_weights(fcoord, w0, w1, w2, w3);
    
    float2 s0 = w0 + w1;
    float2 s1 = w2 + w3;
    float2 f0 = w1 / (w0 + w1);
    float2 f1 = w3 / (w2 + w3);
    
    float2 t0 = (icoord - 1 + f0) * texelSize.xy;
    float2 t1 = (icoord + 1 + f1) * texelSize.xy;
    
    return (SAMPLE_TEXTURE2D(tex, sampler_tex, float2(t0.x, t0.y)) * s0.x +
            SAMPLE_TEXTURE2D(tex, sampler_tex, float2(t1.x, t0.y)) * s1.x) * s0.y +
           (SAMPLE_TEXTURE2D(tex, sampler_tex, float2(t0.x, t1.y)) * s0.x +
            SAMPLE_TEXTURE2D(tex, sampler_tex, float2(t1.x, t1.y)) * s1.x) * s1.y;
}

void cubic_weights(float2 f, out float2 w0, out float2 w1, out float2 w2, out float2 w3)
{
    float2 f2 = f * f;
    float2 f3 = f2 * f;
    
    w0 = -0.5 * f3 + f2 - 0.5 * f;
    w1 = 1.5 * f3 - 2.5 * f2 + 1.0;
    w2 = -1.5 * f3 + 2.0 * f2 + 0.5 * f;
    w3 = 0.5 * f3 - 0.5 * f2;
}

// 고급 블렌딩 모드들
float3 BlendOverlay(float3 base, float3 blend)
{
    return base < 0.5 ? 2.0 * base * blend : 1.0 - 2.0 * (1.0 - base) * (1.0 - blend);
}

float3 BlendSoftLight(float3 base, float3 blend)
{
    return blend < 0.5 ? 2.0 * base * blend + base * base * (1.0 - 2.0 * blend) 
                       : sqrt(base) * (2.0 * blend - 1.0) + 2.0 * base * (1.0 - blend);
}

float3 BlendColorDodge(float3 base, float3 blend)
{
    return blend == 1.0 ? blend : min(base / (1.0 - blend), 1.0);
}

float3 BlendColorBurn(float3 base, float3 blend)
{
    return blend == 0.0 ? blend : max((1.0 - ((1.0 - base) / blend)), 0.0);
}

// 고급 거리 함수들 (SDF)
float sdBox(float3 p, float3 b)
{
    float3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

float sdSphere(float3 p, float r)
{
    return length(p) - r;
}

float sdTorus(float3 p, float2 t)
{
    float2 q = float2(length(p.xz) - t.x, p.y);
    return length(q) - t.y;
}

// SDF 연산들
float opUnion(float d1, float d2) { return min(d1, d2); }
float opSubtraction(float d1, float d2) { return max(-d1, d2); }
float opIntersection(float d1, float d2) { return max(d1, d2); }

float opSmoothUnion(float d1, float d2, float k)
{
    float h = clamp(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0);
    return lerp(d2, d1, h) - k * h * (1.0 - h);
}

#endif // ADVANCED_COMMON_INCLUDED
```

#### 2. 고급 포스트프로세싱 셰이더 템플릿

```hlsl
// AdvancedPostProcess.shader
Shader "Hidden/Advanced Post Process Template"
{
    Properties
    {
        [HideInInspector] _BlitTexture ("Source Texture", 2D) = "white" {}  // AdvancedBlitter는 _BlitTexture 바인딩
        [HideInInspector] _Intensity ("Effect Intensity", Float) = 1.0
        [HideInInspector] _Parameters ("Parameters", Vector) = (1,1,1,1)
        [HideInInspector] _ColorParams ("Color Parameters", Vector) = (1,1,1,1)
    }
    
    SubShader
    {
        Tags 
        { 
            "RenderType" = "Opaque" 
            "RenderPipeline" = "UniversalPipeline"
            "Queue" = "Overlay"
        }
        
        Cull Off 
        ZWrite Off 
        ZTest Always
        
        Pass
        {
            Name "Main Effect"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            // 품질 키워드들
            #pragma multi_compile_local _ _HIGH_QUALITY
            #pragma multi_compile_local _ _TEMPORAL_SAMPLING
            #pragma multi_compile_local _ _DITHERING
            
            // 플랫폼별 키워드들
            #pragma multi_compile _ UNITY_COLORSPACE_GAMMA
            #pragma multi_compile_local_fragment _ _USE_FAST_SRGB_LINEAR_CONVERSION
            
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "AdvancedCommon.hlsl"
            
            TEXTURE2D_X(_BlitTexture);          // Blitter 계열 API는 _BlitTexture 바인딩
            SAMPLER(sampler_BlitTexture);
            float4 _BlitTexture_TexelSize;
            
            float _Intensity;
            float4 _Parameters;      // (param1, param2, param3, param4)
            float4 _ColorParams;     // (r, g, b, alpha)
            
            struct Attributes
            {
                float4 positionOS : POSITION;
                float2 texcoord : TEXCOORD0;
            };
            
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float2 texcoord : TEXCOORD0;
                float4 screenPos : TEXCOORD1;
                UNITY_VERTEX_OUTPUT_STEREO
            };
            
            Varyings vert(Attributes input)
            {
                Varyings output;
                UNITY_SETUP_INSTANCE_ID(input);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(output);
                
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                output.texcoord = input.texcoord;
                output.screenPos = ComputeScreenPos(output.positionCS);
                
                return output;
            }
            
            float4 ApplyEffect(float2 uv)
            {
                // 기본 샘플링
                #ifdef _HIGH_QUALITY
                    float4 color = BicubicSample(TEXTURE2D_ARGS(_BlitTexture, sampler_BlitTexture), 
                                               uv, _BlitTexture_TexelSize);
                #else
                    float4 color = SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_BlitTexture, uv);
                #endif
                
                // 효과 적용
                float3 hsv = RGBToHSV(color.rgb);
                
                // 파라미터 기반 조정
                hsv.x = frac(hsv.x + _Parameters.x * _Intensity); // 색조 시프트
                hsv.y = saturate(hsv.y * (1.0 + _Parameters.y * _Intensity)); // 채도 조정
                hsv.z = saturate(hsv.z * (1.0 + _Parameters.z * _Intensity)); // 밝기 조정
                
                color.rgb = HSVToRGB(hsv);
                
                // 색상 틴트 적용
                color.rgb *= _ColorParams.rgb;
                
                // 디더링 (밴딩 방지)
                #ifdef _DITHERING
                    float dither = hash21(uv * _ScreenParams.xy) - 0.5;
                    color.rgb += dither * (1.0 / 255.0);
                #endif
                
                return color;
            }
            
            float4 frag(Varyings input) : SV_Target
            {
                UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input);
                
                float2 uv = input.texcoord;
                float4 result = ApplyEffect(uv);
                
                #ifdef _TEMPORAL_SAMPLING
                    // 시간 기반 노이즈 추가 (필름 그레인 효과)
                    float2 screenUV = input.screenPos.xy / input.screenPos.w;
                    float temporal = hash21(screenUV + _Time.y);
                    result.rgb += (temporal - 0.5) * 0.02 * _Intensity;
                #endif
                
                // 최종 강도 적용
                result = lerp(SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_BlitTexture, uv), result, _Intensity);
                
                return result;
            }
            
            ENDHLSL
        }
        
        Pass
        {
            Name "Debug Visualization"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragDebug
            
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "AdvancedCommon.hlsl"
            
            // 동일한 입력 구조체들 사용
            
            float4 fragDebug(Varyings input) : SV_Target
            {
                float2 uv = input.texcoord;
                float4 original = SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_BlitTexture, uv);
                
                // 디버그 시각화 (HSV 채널별 표시)
                float3 hsv = RGBToHSV(original.rgb);
                
                // 화면을 4분할해서 각각 다른 정보 표시
                float2 quad = floor(uv * 2.0);
                
                if (quad.x == 0 && quad.y == 1) // 좌상: 원본
                    return original;
                else if (quad.x == 1 && quad.y == 1) // 우상: 색조
                    return float4(hsv.xxx, 1.0);
                else if (quad.x == 0 && quad.y == 0) // 좌하: 채도
                    return float4(hsv.yyy, 1.0);
                else // 우하: 밝기
                    return float4(hsv.zzz, 1.0);
            }
            
            ENDHLSL
        }
    }
    
    FallBack "Hidden/Core/FallbackError"
}
```

---

## 고급 최적화 기법

### GPU 메모리 관리 최적화

#### 1. 스마트 텍스처 포맷 선택

```csharp
public static class OptimalFormatSelector
{
    private struct FormatScore
    {
        public GraphicsFormat format;
        public int score;
        public string reason;
    }
    
    public static GraphicsFormat SelectOptimalHDRFormat(RenderTextureDescriptor baseDesc, 
                                                      bool preserveAlpha = false)
    {
        var candidates = new List<FormatScore>();
        
        // R11G11B10 - 최고 성능 (알파 없음)
        if (!preserveAlpha && SystemInfo.IsFormatSupported(GraphicsFormat.B10G11R11_UFloatPack32, FormatUsage.Render))
        {
            candidates.Add(new FormatScore
            {
                format = GraphicsFormat.B10G11R11_UFloatPack32,
                score = 100,
                reason = "Optimal HDR format, no alpha"
            });
        }
        
        // RGBA16 Half - 균형잡힌 품질/성능
        if (SystemInfo.IsFormatSupported(GraphicsFormat.R16G16B16A16_SFloat, FormatUsage.Render))
        {
            candidates.Add(new FormatScore
            {
                format = GraphicsFormat.R16G16B16A16_SFloat,
                score = preserveAlpha ? 90 : 70,
                reason = "Good quality, supports alpha"
            });
        }
        
        // RGBA32 Float - 최고 품질 (성능 비용 높음)
        if (SystemInfo.IsFormatSupported(GraphicsFormat.R32G32B32A32_SFloat, FormatUsage.Render))
        {
            candidates.Add(new FormatScore
            {
                format = GraphicsFormat.R32G32B32A32_SFloat,
                score = 50,
                reason = "Maximum precision, high memory cost"
            });
        }
        
        // 플랫폼별 특수 포맷
        #if UNITY_ANDROID || UNITY_IOS
        // 모바일에서는 메모리 절약 우선
        if (SystemInfo.IsFormatSupported(GraphicsFormat.R10G10B10A2_UNorm, FormatUsage.Render))
        {
            candidates.Add(new FormatScore
            {
                format = GraphicsFormat.R10G10B10A2_UNorm,
                score = 80,
                reason = "Mobile optimized format"
            });
        }
        #endif
        
        // 최고 점수 포맷 선택
        var bestFormat = candidates.OrderByDescending(c => c.score).FirstOrDefault();
        
        #if UNITY_EDITOR
        Debug.Log($"Selected format: {bestFormat.format}, Reason: {bestFormat.reason}");
        #endif
        
        return bestFormat.format != default ? bestFormat.format : GraphicsFormat.R16G16B16A16_SFloat;
    }
    
    public static GraphicsFormat SelectOptimalLDRFormat(bool needsAlpha, bool isSRGB = true)
    {
        if (needsAlpha)
        {
            return isSRGB ? GraphicsFormat.R8G8B8A8_SRGB : GraphicsFormat.R8G8B8A8_UNorm;
        }
        else
        {
            // RGB565 모바일에서 메모리 절약 (알파 불필요시)
            #if UNITY_ANDROID || UNITY_IOS
            if (SystemInfo.IsFormatSupported(GraphicsFormat.R5G6B5_UNormPack16, FormatUsage.Render))
            {
                return GraphicsFormat.R5G6B5_UNormPack16;
            }
            #endif
            
            return isSRGB ? GraphicsFormat.R8G8B8A8_SRGB : GraphicsFormat.R8G8B8A8_UNorm;
        }
    }
    
    public static GraphicsFormat SelectDepthFormat(bool needsStencil = false, bool highPrecision = false)
    {
        if (needsStencil)
        {
            if (highPrecision && SystemInfo.IsFormatSupported(GraphicsFormat.D32_SFloat_S8_UInt, FormatUsage.Render))
                return GraphicsFormat.D32_SFloat_S8_UInt;
            else if (SystemInfo.IsFormatSupported(GraphicsFormat.D24_UNorm_S8_UInt, FormatUsage.Render))
                return GraphicsFormat.D24_UNorm_S8_UInt;
            else
                return GraphicsFormat.D16_UNorm;
        }
        else
        {
            if (highPrecision && SystemInfo.IsFormatSupported(GraphicsFormat.D32_SFloat, FormatUsage.Render))
                return GraphicsFormat.D32_SFloat;
            else
                return GraphicsFormat.D16_UNorm;
        }
    }
}
```

#### 2. 동적 해상도 스케일링

```csharp
public class AdaptiveResolutionController
{
    private struct PerformanceMetrics
    {
        public float frameTime;
        public float gpuTime;
        public int droppedFrames;
        public float temperature; // 모바일 디바이스 온도 (가능한 경우)
    }
    
    private readonly Queue<PerformanceMetrics> m_MetricsHistory = new();
    private readonly int m_MaxHistorySize = 30; // 30프레임 기록
    private float m_CurrentScale = 1.0f;
    private float m_TargetFPS = 60f;
    private float m_MinScale = 0.5f;
    private float m_MaxScale = 1.0f;
    
    public float CurrentScale => m_CurrentScale;
    public bool IsActive => m_CurrentScale < 1.0f;
    
    public void UpdateMetrics(float frameTime, float gpuTime)
    {
        var metrics = new PerformanceMetrics
        {
            frameTime = frameTime,
            gpuTime = gpuTime,
            droppedFrames = Application.targetFrameRate > 0 && frameTime > (1f / Application.targetFrameRate) ? 1 : 0,
            #if UNITY_ANDROID
            temperature = SystemInfo.batteryTemperature
            #endif
        };
        
        m_MetricsHistory.Enqueue(metrics);
        if (m_MetricsHistory.Count > m_MaxHistorySize)
            m_MetricsHistory.Dequeue();
        
        UpdateResolutionScale();
    }
    
    private void UpdateResolutionScale()
    {
        if (m_MetricsHistory.Count < 10) // 충분한 데이터가 쌓일 때까지 대기
            return;
            
        var recentMetrics = m_MetricsHistory.TakeLast(10).ToArray();
        var averageFrameTime = recentMetrics.Average(m => m.frameTime);
        var droppedFrameRate = recentMetrics.Average(m => m.droppedFrames);
        
        float targetFrameTime = 1f / m_TargetFPS;
        float performanceRatio = targetFrameTime / averageFrameTime;
        
        // 성능 기반 스케일 조정
        float desiredScale = m_CurrentScale;
        
        if (performanceRatio < 0.85f) // 성능이 85% 이하로 떨어지면 해상도 감소
        {
            desiredScale = Mathf.Max(m_CurrentScale * 0.9f, m_MinScale);
        }
        else if (performanceRatio > 1.1f && droppedFrameRate < 0.1f) // 성능 여유가 있으면 해상도 증가
        {
            desiredScale = Mathf.Min(m_CurrentScale * 1.05f, m_MaxScale);
        }
        
        // 온도 기반 추가 조정 (모바일)
        #if UNITY_ANDROID
        var averageTemp = recentMetrics.Average(m => m.temperature);
        if (averageTemp > 45f) // 45도 이상이면 강제 다운스케일
        {
            desiredScale = Mathf.Min(desiredScale, 0.75f);
        }
        #endif
        
        // 부드러운 전환
        m_CurrentScale = Mathf.Lerp(m_CurrentScale, desiredScale, Time.deltaTime * 2f);
    }
    
    public Vector2Int GetScaledResolution(Vector2Int baseResolution)
    {
        return new Vector2Int(
            Mathf.RoundToInt(baseResolution.x * m_CurrentScale),
            Mathf.RoundToInt(baseResolution.y * m_CurrentScale)
        );
    }
    
    public void SetTargetFPS(float targetFPS)
    {
        m_TargetFPS = targetFPS;
    }
    
    public void SetScaleRange(float minScale, float maxScale)
    {
        m_MinScale = Mathf.Clamp01(minScale);
        m_MaxScale = Mathf.Clamp01(maxScale);
        m_CurrentScale = Mathf.Clamp(m_CurrentScale, m_MinScale, m_MaxScale);
    }
}
```

---

## 플랫폼별 구현 전략

### 모바일 최적화

#### 1. 모바일 특화 셰이더 변형

```hlsl
// MobileOptimizedShader.shader
Shader "Hidden/Mobile Optimized Post Process"
{
    Properties
    {
        [HideInInspector] _MainTex ("Source Texture", 2D) = "white" {}
        [HideInInspector] _Intensity ("Intensity", Range(0,1)) = 1.0
    }
    
    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" }
        
        Pass
        {
            Name "Mobile Optimized"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            // 모바일 특화 키워드들
            #pragma multi_compile _ SHADER_API_MOBILE
            #pragma multi_compile_local _ _QUALITY_LOW _QUALITY_MEDIUM
            
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            
            TEXTURE2D(_MainTex);
            SAMPLER(sampler_MainTex);
            half _Intensity;
            
            struct Attributes
            {
                float4 positionOS : POSITION;
                float2 texcoord : TEXCOORD0;
            };
            
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float2 texcoord : TEXCOORD0;
            };
            
            Varyings vert(Attributes input)
            {
                Varyings output;
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                output.texcoord = input.texcoord;
                return output;
            }
            
            half4 frag(Varyings input) : SV_Target
            {
                half4 color = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord);
                
                #if defined(SHADER_API_MOBILE)
                    // 모바일에서는 half 정밀도 사용
                    #if defined(_QUALITY_LOW)
                        // 저품질: 간단한 채도 조정만
                        color.rgb = lerp(dot(color.rgb, half3(0.299, 0.587, 0.114)).xxx, 
                                        color.rgb, 1.0 + _Intensity * 0.5);
                    #elif defined(_QUALITY_MEDIUM)
                        // 중간품질: 기본적인 색상 보정
                        half3 hsv = RGBToHSV_Fast(color.rgb);
                        hsv.y *= 1.0 + _Intensity * 0.3;
                        color.rgb = HSVToRGB_Fast(hsv);
                    #else
                        // 기본품질: 전체 효과 적용
                        color.rgb = ApplyMobileEffect(color.rgb, _Intensity);
                    #endif
                #else
                    // 데스크톱에서는 풀 효과
                    color.rgb = ApplyFullEffect(color.rgb, _Intensity);
                #endif
                
                return color;
            }
            
            // 모바일 최적화된 HSV 변환 (근사치)
            half3 RGBToHSV_Fast(half3 rgb)
            {
                half maxComponent = max(max(rgb.r, rgb.g), rgb.b);
                half minComponent = min(min(rgb.r, rgb.g), rgb.b);
                half delta = maxComponent - minComponent;
                
                half hue = 0.0;
                if (delta > 0.001)
                {
                    if (maxComponent == rgb.r)
                        hue = frac((rgb.g - rgb.b) / delta * 0.166667);
                    else if (maxComponent == rgb.g)
                        hue = frac((rgb.b - rgb.r) / delta * 0.166667 + 0.333333);
                    else
                        hue = frac((rgb.r - rgb.g) / delta * 0.166667 + 0.666667);
                }
                
                half saturation = maxComponent > 0.001 ? delta / maxComponent : 0.0;
                half value = maxComponent;
                
                return half3(hue, saturation, value);
            }
            
            half3 HSVToRGB_Fast(half3 hsv)
            {
                half c = hsv.z * hsv.y;
                half x = c * (1.0 - abs(fmod(hsv.x * 6.0, 2.0) - 1.0));
                half m = hsv.z - c;
                
                half3 rgb;
                if (hsv.x < 0.166667)      rgb = half3(c, x, 0);
                else if (hsv.x < 0.333333) rgb = half3(x, c, 0);
                else if (hsv.x < 0.5)      rgb = half3(0, c, x);
                else if (hsv.x < 0.666667) rgb = half3(0, x, c);
                else if (hsv.x < 0.833333) rgb = half3(x, 0, c);
                else                       rgb = half3(c, 0, x);
                
                return rgb + m;
            }
            
            half3 ApplyMobileEffect(half3 color, half intensity)
            {
                // 모바일 최적화된 색상 효과
                half luminance = dot(color, half3(0.299, 0.587, 0.114));
                color = lerp(luminance.xxx, color, 1.0 + intensity * 0.5);
                return color;
            }
            
            half3 ApplyFullEffect(half3 color, half intensity)
            {
                // 전체 품질 효과 (데스크톱용)
                return color * (1.0 + intensity);
            }
            
            ENDHLSL
        }
    }
    
    FallBack "Hidden/Core/FallbackError"
}
```

#### 2. 플랫폼별 자동 품질 조정

```csharp
public static class PlatformQualityManager
{
    private static Dictionary<string, QualityProfile> s_DeviceProfiles;
    
    [RuntimeInitializeOnLoadMethod]
    private static void Initialize()
    {
        BuildDeviceProfiles();
        ApplyOptimalQuality();
    }
    
    private static void BuildDeviceProfiles()
    {
        s_DeviceProfiles = new Dictionary<string, QualityProfile>();
        
        // iPhone 프로필들
        s_DeviceProfiles["iPhone14,2"] = new QualityProfile // iPhone 13 Pro
        {
            renderScale = 0.9f,
            shadowDistance = 50f,
            shadowCascades = 2,
            postProcessingQuality = QualityPreset.High,
            enableMSAA = false,
            textureQuality = 0
        };
        
        s_DeviceProfiles["iPhone13,2"] = new QualityProfile // iPhone 12
        {
            renderScale = 0.8f,
            shadowDistance = 30f,
            shadowCascades = 1,
            postProcessingQuality = QualityPreset.Medium,
            enableMSAA = false,
            textureQuality = 1
        };
        
        // Android 프로필들 (GPU별)
        s_DeviceProfiles["Adreno (TM) 730"] = new QualityProfile // Snapdragon 8 Gen 1
        {
            renderScale = 0.85f,
            shadowDistance = 40f,
            shadowCascades = 2,
            postProcessingQuality = QualityPreset.High,
            enableMSAA = false,
            textureQuality = 0
        };
        
        s_DeviceProfiles["Mali-G78"] = new QualityProfile // Samsung Exynos
        {
            renderScale = 0.75f,
            shadowDistance = 25f,
            shadowCascades = 1,
            postProcessingQuality = QualityPreset.Medium,
            enableMSAA = false,
            textureQuality = 1
        };
    }
    
    public static void ApplyOptimalQuality()
    {
        var profile = GetDeviceProfile();
        
        // URP Asset 설정 조정
        if (UniversalRenderPipeline.asset != null)
        {
            var urpAsset = UniversalRenderPipeline.asset;
            urpAsset.renderScale = profile.renderScale;
            urpAsset.shadowDistance = profile.shadowDistance;
            urpAsset.shadowCascadeCount = profile.shadowCascades;
            urpAsset.msaaSampleCount = profile.enableMSAA ? 4 : 1;
        }
        
        // Unity 품질 설정
        QualitySettings.masterTextureLimit = profile.textureQuality;
        QualitySettings.shadows = profile.shadowCascades > 0 ? ShadowQuality.All : ShadowQuality.Disable;
        
        // 플랫폼별 추가 최적화
        #if UNITY_ANDROID
        ApplyAndroidOptimizations(profile);
        #elif UNITY_IOS
        ApplyIOSOptimizations(profile);
        #endif
    }
    
    private static QualityProfile GetDeviceProfile()
    {
        string deviceKey = SystemInfo.deviceModel;
        
        #if UNITY_ANDROID
        // Android에서는 GPU 이름 사용
        deviceKey = SystemInfo.graphicsDeviceName;
        #endif
        
        if (s_DeviceProfiles.TryGetValue(deviceKey, out var profile))
        {
            return profile;
        }
        
        // 기본 프로필 (성능 기반 추정)
        return EstimateQualityProfile();
    }
    
    private static QualityProfile EstimateQualityProfile()
    {
        var profile = new QualityProfile();
        
        // 메모리 기반 추정
        int systemMemoryMB = SystemInfo.systemMemorySize;
        int graphicsMemoryMB = SystemInfo.graphicsMemorySize;
        
        if (systemMemoryMB >= 8192 && graphicsMemoryMB >= 2048) // 고사양
        {
            profile.renderScale = 1.0f;
            profile.postProcessingQuality = QualityPreset.High;
            profile.shadowCascades = 4;
            profile.enableMSAA = true;
        }
        else if (systemMemoryMB >= 4096 && graphicsMemoryMB >= 1024) // 중사양
        {
            profile.renderScale = 0.85f;
            profile.postProcessingQuality = QualityPreset.Medium;
            profile.shadowCascades = 2;
            profile.enableMSAA = false;
        }
        else // 저사양
        {
            profile.renderScale = 0.7f;
            profile.postProcessingQuality = QualityPreset.Low;
            profile.shadowCascades = 1;
            profile.enableMSAA = false;
            profile.textureQuality = 2;
        }
        
        return profile;
    }
    
    #if UNITY_ANDROID
    private static void ApplyAndroidOptimizations(QualityProfile profile)
    {
        // Android 특화 최적화
        Screen.sleepTimeout = SleepTimeout.NeverSleep;
        Application.targetFrameRate = profile.postProcessingQuality >= QualityPreset.High ? 60 : 30;
        
        // 배터리 최적화 모드 감지 및 대응
        if (Application.isMobilePlatform && SystemInfo.batteryLevel < 0.3f)
        {
            // 배터리 부족시 성능 다운
            profile.renderScale *= 0.8f;
            Application.targetFrameRate = 30;
        }
    }
    #endif
    
    #if UNITY_IOS
    private static void ApplyIOSOptimizations(QualityProfile profile)
    {
        // iOS 특화 최적화
        Application.targetFrameRate = 60; // iOS는 항상 60FPS 목표
        
        // Metal 성능 튜닝
        if (SystemInfo.graphicsDeviceType == GraphicsDeviceType.Metal)
        {
            // Metal 특화 설정
            QualitySettings.vSyncCount = 1;
        }
    }
    #endif
}

[Serializable]
public class QualityProfile
{
    public float renderScale = 1.0f;
    public float shadowDistance = 50f;
    public int shadowCascades = 2;
    public QualityPreset postProcessingQuality = QualityPreset.Medium;
    public bool enableMSAA = false;
    public int textureQuality = 0;
}
```

---

## 실전 구현 예제

### 완전한 커스텀 포스트프로세싱 시스템

이제 지금까지 학습한 모든 내용을 종합하여 실제 프로덕션에서 사용할 수 있는 완전한 시스템을 구현해보겠습니다:

#### 1. 통합 렌더링 시스템

```csharp
public class IntegratedPostProcessingSystem : IDisposable
{
    private readonly Dictionary<Type, IPostProcessEffect> m_Effects = new();
    private readonly AdaptiveResolutionController m_ResolutionController = new();
    private readonly AdvancedProfiler m_Profiler = new();
    private readonly ManagedTexturePool m_TexturePool = new();
    
    private VolumeStack m_VolumeStack;
    private bool m_IsInitialized;
    
    public void Initialize()
    {
        if (m_IsInitialized) return;
        
        // Volume Stack 설정
        m_VolumeStack = VolumeManager.instance.stack;
        
        // 기본 효과들 등록
        RegisterEffect<ComplexEffect>(new ComplexPostProcessEffect());
        RegisterEffect<VintageFilm>(new VintageFilmEffect());
        
        // 플랫폼별 품질 설정
        PlatformQualityManager.ApplyOptimalQuality();
        
        m_IsInitialized = true;
    }
    
    public void RegisterEffect<T>(IPostProcessEffect effect) where T : VolumeComponent
    {
        m_Effects[typeof(T)] = effect;
    }
    
    public void ExecutePostProcessing(RenderGraph renderGraph, 
                                    UniversalResourceData resourceData,
                                    UniversalCameraData cameraData)
    {
        if (!m_IsInitialized) return;
        
        using (m_Profiler.BeginSample("Post Processing System"))
        {
            // 적응형 해상도 계산
            var scaledResolution = m_ResolutionController.GetScaledResolution(
                new Vector2Int(cameraData.cameraTargetDescriptor.width, 
                             cameraData.cameraTargetDescriptor.height));
            
            var currentInput = resourceData.activeColorTexture;
            
            // 활성화된 효과들 수집 및 실행
            var activeEffects = GetActiveEffects();
            
            foreach (var effectPair in activeEffects)
            {
                var volumeComponent = effectPair.Key;
                var effect = effectPair.Value;
                
                using (m_Profiler.BeginSample($"Effect: {volumeComponent.GetType().Name}"))
                {
                    var outputTexture = effect.Execute(renderGraph, currentInput, 
                                                     volumeComponent, scaledResolution);
                    if (outputTexture.IsValid())
                    {
                        currentInput = outputTexture;
                    }
                }
            }
            
            // 최종 결과를 활성 컬러 텍스처로 복사
            if (currentInput != resourceData.activeColorTexture)
            {
                CopyToActiveTexture(renderGraph, currentInput, resourceData);
            }
        }
        
        // 성능 메트릭 업데이트
        m_ResolutionController.UpdateMetrics(Time.deltaTime, GetGPUTime());
    }
    
    private List<(VolumeComponent, IPostProcessEffect)> GetActiveEffects()
    {
        var activeEffects = new List<(VolumeComponent, IPostProcessEffect)>();
        
        foreach (var effectType in m_Effects.Keys)
        {
            var component = m_VolumeStack.GetComponent(effectType);
            if (component != null && IsComponentActive(component))
            {
                activeEffects.Add((component, m_Effects[effectType]));
            }
        }
        
        // 실행 순서 정렬 (우선순위 기반)
        activeEffects.Sort((a, b) => GetEffectPriority(a.Item1).CompareTo(GetEffectPriority(b.Item1)));
        
        return activeEffects;
    }
    
    private bool IsComponentActive(VolumeComponent component)
    {
        return component.active && 
               (component is IPostProcessComponent postProcess ? postProcess.IsActive() : true);
    }
    
    private int GetEffectPriority(VolumeComponent component)
    {
        // 효과 타입별 우선순위 (낮은 숫자가 먼저 실행)
        return component switch
        {
            ComplexEffect => 100,
            VintageFilm => 200,
            _ => 1000
        };
    }
    
    private void CopyToActiveTexture(RenderGraph renderGraph, TextureHandle source, 
                                   UniversalResourceData resourceData)
    {
        using (var builder = renderGraph.AddRasterRenderPass<CopyPassData>("Final Copy", out var passData))
        {
            passData.source = builder.UseTexture(source, AccessFlags.Read);
            passData.destination = builder.SetRenderAttachment(resourceData.activeColorTexture, 0, AccessFlags.WriteAll);
            
            builder.SetRenderFunc(static (CopyPassData data, RasterGraphContext context) =>
            {
                Blitter.BlitCameraTexture(context.cmd, data.source, data.destination);
            });
        }
    }
    
    private float GetGPUTime()
    {
        // GPU 시간 측정 (플랫폼별 구현)
        #if UNITY_EDITOR
        return UnityEditor.UnityStats.frameTime;
        #else
        return Time.deltaTime; // 근사치
        #endif
    }
    
    public void Dispose()
    {
        m_Profiler?.Dispose();
        m_TexturePool?.ClearPool();
        
        foreach (var effect in m_Effects.Values)
        {
            if (effect is IDisposable disposable)
                disposable.Dispose();
        }
        
        m_Effects.Clear();
        m_IsInitialized = false;
    }
}

// 효과 인터페이스
public interface IPostProcessEffect
{
    TextureHandle Execute(RenderGraph renderGraph, TextureHandle input, 
                         VolumeComponent settings, Vector2Int targetResolution);
}

private class CopyPassData
{
    internal TextureHandle source;
    internal TextureHandle destination;
}
```

이 가이드는 Unity 6.0 렌더링 파이프라인 코어의 모든 주요 시스템을 다루며, 실제 프로덕션 환경에서 사용할 수 있는 고급 기법들을 제공합니다. 특히 Volume System의 깊이 있는 활용과 RenderGraph의 고급 패턴들을 통해 고품질의 포스트프로세싱 효과를 효율적으로 구현할 수 있습니다.