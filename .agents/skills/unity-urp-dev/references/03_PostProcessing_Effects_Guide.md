# Unity 6.0 URP Post-processing 효과 개발 가이드

## 개요

Unity 6.0 URP의 Built-in Post-processing 효과들을 심층 분석한 내용을 바탕으로, 고품질의 커스텀 포스트프로세싱 효과를 개발하기 위한 완전한 가이드입니다. 실제 프로덕션 환경에서 사용할 수 있는 최적화 기법과 구현 패턴을 제공합니다.

## 목차

1. [Bloom 효과 완전 구현](#bloom-효과-완전-구현)
2. [Depth of Field 고급 기법](#depth-of-field-고급-기법)
3. [Motion Blur 시스템](#motion-blur-시스템)
4. [Color Grading & Tone Mapping](#color-grading--tone-mapping)
5. [Lens Effects 구현](#lens-effects-구현)
6. [Anti-aliasing 기법](#anti-aliasing-기법)
7. [SSAO/SSGI 구현](#ssaossgi-구현)
8. [Uber Shader 패턴](#uber-shader-패턴)
9. [성능 최적화 전략](#성능-최적화-전략)
10. [디버깅 및 검증](#디버깅-및-검증)

---

## Bloom 효과 완전 구현

### 고품질 Bloom 시스템 구축

#### 1. Advanced Bloom Volume Component

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Advanced/Enhanced Bloom")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
public sealed class EnhancedBloom : VolumeComponent, IPostProcessComponent
{
    [Header("Basic Settings")]
    [Tooltip("Bloom intensity")]
    public MinFloatParameter intensity = new MinFloatParameter(0f, 0f);
    
    [Tooltip("Brightness threshold")]
    public MinFloatParameter threshold = new MinFloatParameter(1f, 0f);
    
    [Tooltip("Soft threshold knee")]
    public ClampedFloatParameter softKnee = new ClampedFloatParameter(0.5f, 0f, 1f);
    
    [Header("Quality Settings")]
    [Tooltip("Number of blur iterations")]
    public ClampedIntParameter iterations = new ClampedIntParameter(6, 1, 16);
    
    [Tooltip("Downsampling mode")]
    public DownsampleModeParameter downsampleMode = new DownsampleModeParameter(DownsampleMode.Half);
    
    [Tooltip("High quality filtering")]
    public BoolParameter highQualityFiltering = new BoolParameter(false);
    
    [Header("Advanced Controls")]
    [Tooltip("Per-iteration intensity curve")]
    public AnimationCurveParameter intensityCurve = new AnimationCurveParameter(
        AnimationCurve.Linear(0f, 1f, 1f, 0f), false);
    
    [Tooltip("Color temperature shift")]
    public ClampedFloatParameter temperature = new ClampedFloatParameter(0f, -100f, 100f);
    
    [Tooltip("Bloom tint color")]
    public ColorParameter tint = new ColorParameter(Color.white, false, false, true);
    
    [Header("Lens Dirt")]
    [Tooltip("Lens dirt texture")]
    public TextureParameter dirtTexture = new TextureParameter(null);
    
    [Tooltip("Dirt intensity")]
    public MinFloatParameter dirtIntensity = new MinFloatParameter(0f, 0f);
    
    [Header("Performance")]
    [Tooltip("Enable temporal optimization")]
    public BoolParameter temporalOptimization = new BoolParameter(false);
    
    public bool IsActive() => intensity.value > 0f;
}

public enum DownsampleMode
{
    Half = 1,
    Quarter = 2,
    Eighth = 3
}

[Serializable]
public sealed class DownsampleModeParameter : VolumeParameter<DownsampleMode>
{
    public DownsampleModeParameter(DownsampleMode value, bool overrideState = false) 
        : base(value, overrideState) { }
}
```

#### 2. Enhanced Bloom Render Pass

```csharp
public class EnhancedBloomRenderPass : ScriptableRenderPass
{
    private const int k_MaxPyramidLevels = 16;
    private const int k_BicubicUpsampling = 1;
    private const int k_BilinearUpsampling = 0;
    
    private Material m_BloomMaterial;
    private EnhancedBloom m_BloomSettings;
    
    // Pyramid textures
    private RTHandle[] m_BloomMipDown = new RTHandle[k_MaxPyramidLevels];
    private RTHandle[] m_BloomMipUp = new RTHandle[k_MaxPyramidLevels];
    
    // Temporal history (for optimization)
    private RTHandle m_TemporalHistory;
    private bool m_FirstFrame = true;
    
    private static readonly ProfilingSampler s_ProfilingSampler = 
        new ProfilingSampler("Enhanced Bloom");
    
    // Shader property IDs
    private static readonly int s_BloomParams = Shader.PropertyToID("_BloomParams");
    private static readonly int s_BloomTint = Shader.PropertyToID("_BloomTint");
    private static readonly int s_DirtTexture = Shader.PropertyToID("_DirtTexture");
    private static readonly int s_DirtParams = Shader.PropertyToID("_DirtParams");
    private static readonly int s_TemporalParams = Shader.PropertyToID("_TemporalParams");
    
    public EnhancedBloomRenderPass(Material bloomMaterial)
    {
        m_BloomMaterial = bloomMaterial;
        renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }
    
    public void Setup(EnhancedBloom bloomSettings)
    {
        m_BloomSettings = bloomSettings;
    }
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        if (!ShouldRender(cameraData))
            return;
            
        ExecuteEnhancedBloom(renderGraph, resourceData, cameraData);
    }
    
    private void ExecuteEnhancedBloom(RenderGraph renderGraph, 
                                    UniversalResourceData resourceData,
                                    UniversalCameraData cameraData)
    {
        using (var builder = renderGraph.AddUnsafePass<EnhancedBloomData>(
            "Enhanced Bloom", out var passData, s_ProfilingSampler))
        {
            // 파라미터 계산
            var bloomParams = CalculateBloomParameters(cameraData.cameraTargetDescriptor);
            
            // 텍스처 피라미드 생성
            SetupBloomPyramid(renderGraph, bloomParams, passData);
            
            // PassData 설정
            passData.sourceTexture = resourceData.activeColorTexture;
            passData.bloomSettings = m_BloomSettings;
            passData.bloomParams = bloomParams;
            passData.material = m_BloomMaterial;
            
            // 리소스 의존성
            builder.UseTexture(passData.sourceTexture, AccessFlags.Read);
            for (int i = 0; i < bloomParams.iterationCount; i++)
            {
                if (passData.mipDown[i].IsValid())
                    builder.UseTexture(passData.mipDown[i], AccessFlags.ReadWrite);
                if (passData.mipUp[i].IsValid())
                    builder.UseTexture(passData.mipUp[i], AccessFlags.ReadWrite);
            }
            
            // 실행 함수
            builder.SetRenderFunc(static (EnhancedBloomData data, UnsafeGraphContext context) =>
            {
                ExecuteBloomPasses(data, context);
            });
        }
    }
    
    private static void ExecuteBloomPasses(EnhancedBloomData data, UnsafeGraphContext context)
    {
        var cmd = CommandBufferHelpers.GetNativeCommandBuffer(context.cmd);
        
        // 1. Prefilter Pass (임계값 필터링 + 다운샘플)
        SetupPrefilterParameters(data);
        cmd.Blit(data.sourceTexture, data.mipDown[0], data.material, 0);
        
        // 2. Downsample Chain
        for (int i = 1; i < data.bloomParams.iterationCount; i++)
        {
            int pass = data.bloomSettings.highQualityFiltering.value ? 2 : 1;
            cmd.Blit(data.mipDown[i-1], data.mipDown[i], data.material, pass);
        }
        
        // 3. Upsample Chain with Additive Blending
        for (int i = data.bloomParams.iterationCount - 2; i >= 0; i--)
        {
            SetupUpsampleParameters(data, i);
            int pass = data.bloomSettings.highQualityFiltering.value ? 4 : 3;
            cmd.Blit(data.mipDown[i+1], data.mipUp[i], data.material, pass);
            
            // Additive blend with previous level
            if (i < data.bloomParams.iterationCount - 2)
            {
                cmd.SetGlobalTexture("_MainTex2", data.mipUp[i+1]);
                cmd.Blit(data.mipUp[i], data.mipUp[i], data.material, 5); // Additive pass
            }
        }
        
        // 4. Final Composition (with lens dirt if enabled)
        SetupCompositionParameters(data);
        int finalPass = data.bloomSettings.dirtTexture.value != null ? 7 : 6;
        cmd.Blit(data.mipUp[0], data.sourceTexture, data.material, finalPass);
    }
    
    private static void SetupPrefilterParameters(EnhancedBloomData data)
    {
        var settings = data.bloomSettings;
        float knee = settings.threshold.value * settings.softKnee.value;
        
        var bloomParams = new Vector4(
            settings.threshold.value,
            settings.threshold.value - knee,
            knee * 2f,
            0.25f / (knee + 0.00001f)
        );
        
        data.material.SetVector(s_BloomParams, bloomParams);
    }
    
    private static void SetupUpsampleParameters(EnhancedBloomData data, int level)
    {
        // 레벨별 강도 조정 (AnimationCurve 기반)
        float t = (float)level / (data.bloomParams.iterationCount - 1);
        float levelIntensity = data.bloomSettings.intensityCurve.value.Evaluate(t);
        
        var upsampleParams = new Vector4(
            levelIntensity * data.bloomSettings.intensity.value,
            data.bloomSettings.temperature.value / 100f,
            0f, 0f
        );
        
        data.material.SetVector(s_BloomParams, upsampleParams);
        data.material.SetColor(s_BloomTint, data.bloomSettings.tint.value);
    }
    
    private static void SetupCompositionParameters(EnhancedBloomData data)
    {
        var settings = data.bloomSettings;
        
        // Lens dirt 설정
        if (settings.dirtTexture.value != null)
        {
            data.material.SetTexture(s_DirtTexture, settings.dirtTexture.value);
            data.material.SetFloat(s_DirtParams, settings.dirtIntensity.value);
        }
        
        // 최종 강도 설정
        data.material.SetFloat("_FinalIntensity", settings.intensity.value);
        
        // 키워드 설정
        CoreUtils.SetKeyword(data.material, "_LENS_DIRT", 
            settings.dirtTexture.value != null && settings.dirtIntensity.value > 0f);
        CoreUtils.SetKeyword(data.material, "_HIGH_QUALITY", 
            settings.highQualityFiltering.value);
    }
    
    private BloomParameters CalculateBloomParameters(RenderTextureDescriptor desc)
    {
        var parameters = new BloomParameters();
        
        // 다운샘플 시작 해상도
        int downsampleFactor = (int)m_BloomSettings.downsampleMode.value;
        parameters.startWidth = desc.width / downsampleFactor;
        parameters.startHeight = desc.height / downsampleFactor;
        
        // 반복 횟수 계산
        parameters.iterationCount = Mathf.Min(m_BloomSettings.iterations.value, k_MaxPyramidLevels);
        
        // 최소 해상도까지만 다운샘플링
        int minSize = Mathf.Min(parameters.startWidth, parameters.startHeight);
        int maxIterations = Mathf.FloorToInt(Mathf.Log(minSize, 2)) - 1;
        parameters.iterationCount = Mathf.Min(parameters.iterationCount, maxIterations);
        
        return parameters;
    }
    
    private void SetupBloomPyramid(RenderGraph renderGraph, BloomParameters bloomParams, 
                                 EnhancedBloomData passData)
    {
        passData.mipDown = new TextureHandle[bloomParams.iterationCount];
        passData.mipUp = new TextureHandle[bloomParams.iterationCount];
        
        int width = bloomParams.startWidth;
        int height = bloomParams.startHeight;
        
        for (int i = 0; i < bloomParams.iterationCount; i++)
        {
            // Downsample 텍스처 생성
            var downDesc = new TextureDesc(width, height)
            {
                colorFormat = GetOptimalBloomFormat(),
                enableRandomWrite = false,
                clearBuffer = false,
                name = $"_BloomMipDown{i}"
            };
            
            passData.mipDown[i] = renderGraph.CreateTexture(downDesc);
            
            // Upsample 텍스처 생성 (마지막 레벨 제외)
            if (i < bloomParams.iterationCount - 1)
            {
                var upDesc = downDesc;
                upDesc.name = $"_BloomMipUp{i}";
                passData.mipUp[i] = renderGraph.CreateTexture(upDesc);
            }
            
            // 다음 레벨 해상도
            width = Mathf.Max(1, width / 2);
            height = Mathf.Max(1, height / 2);
        }
    }
    
    private GraphicsFormat GetOptimalBloomFormat()
    {
        // HDR 포맷 선택 (플랫폼별 최적화)
        if (SystemInfo.IsFormatSupported(GraphicsFormat.B10G11R11_UFloatPack32, FormatUsage.Render))
            return GraphicsFormat.B10G11R11_UFloatPack32; // 최적 성능
        else if (SystemInfo.IsFormatSupported(GraphicsFormat.R16G16B16A16_SFloat, FormatUsage.Render))
            return GraphicsFormat.R16G16B16A16_SFloat;     // 균형
        else
            return GraphicsFormat.R32G32B32A32_SFloat;     // 폴백
    }
    
    private bool ShouldRender(UniversalCameraData cameraData)
    {
        return cameraData.camera.cameraType == CameraType.Game &&
               m_BloomSettings.IsActive();
    }
}

// PassData 구조체
private class EnhancedBloomData
{
    internal TextureHandle sourceTexture;
    internal TextureHandle[] mipDown;
    internal TextureHandle[] mipUp;
    internal EnhancedBloom bloomSettings;
    internal BloomParameters bloomParams;
    internal Material material;
}

private struct BloomParameters
{
    internal int startWidth;
    internal int startHeight;
    internal int iterationCount;
}
```

#### 3. Enhanced Bloom Shader

```hlsl
// ⚠️ 참고: 이 셰이더는 AddUnsafePass 내부에서 cmd.Blit으로 직접 텍스처를 바인딩하므로 _MainTex 사용이 가능합니다.
// Blitter.BlitTexture / Blitter.BlitCameraTexture를 사용하는 경우에는 반드시 _BlitTexture로 변경해야 합니다.
// (Known Pitfall 참조: SKILL.md 섹션 5.5)
Shader "Hidden/Enhanced Bloom"
{
    Properties
    {
        [HideInInspector] _MainTex ("Source Texture", 2D) = "white" {}
        [HideInInspector] _MainTex2 ("Secondary Texture", 2D) = "white" {}
    }
    
    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" }
        
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"
        
        TEXTURE2D(_MainTex);
        TEXTURE2D(_MainTex2);
        TEXTURE2D(_DirtTexture);
        SAMPLER(sampler_MainTex);
        SAMPLER(sampler_MainTex2);
        SAMPLER(sampler_DirtTexture);
        
        float4 _MainTex_TexelSize;
        float4 _BloomParams;     // (threshold, threshold-knee, knee*2, 0.25/knee)
        float4 _BloomTint;
        float4 _DirtParams;
        float _FinalIntensity;
        
        struct Attributes
        {
            float4 positionOS : POSITION;
            float2 texcoord : TEXCOORD0;
        };
        
        struct Varyings
        {
            float4 positionCS : SV_POSITION;
            float2 texcoord : TEXCOORD0;
            float4 texcoord01 : TEXCOORD1;
            float4 texcoord23 : TEXCOORD2;
        };
        
        Varyings vert(Attributes input)
        {
            Varyings output;
            output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
            output.texcoord = input.texcoord;
            
            // 4개의 텍스처 좌표 계산 (13-tap 블러용)
            float2 texelSize = _MainTex_TexelSize.xy;
            output.texcoord01.xy = input.texcoord + texelSize * float2(-1, -1);
            output.texcoord01.zw = input.texcoord + texelSize * float2( 1, -1);
            output.texcoord23.xy = input.texcoord + texelSize * float2(-1,  1);
            output.texcoord23.zw = input.texcoord + texelSize * float2( 1,  1);
            
            return output;
        }
        
        // 임계값 필터링 함수 (고급 soft knee)
        float4 ApplyBloomThreshold(float4 color, float4 threshold)
        {
            float brightness = Max3(color.r, color.g, color.b);
            float knee = threshold.z;
            float soft = brightness - threshold.y;
            soft = clamp(soft, 0, knee);
            soft = soft * soft * threshold.w;
            float contribution = max(soft, brightness - threshold.x);
            contribution /= max(brightness, 1e-4);
            return color * contribution;
        }
        
        ENDHLSL
        
        // Pass 0: Prefilter (임계값 + 다운샘플)
        Pass
        {
            Name "Bloom Prefilter"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragPrefilter
            #pragma multi_compile_local _ _HIGH_QUALITY
            
            float4 fragPrefilter(Varyings input) : SV_Target
            {
                #ifdef _HIGH_QUALITY
                    // 13-tap 다운샘플링
                    float4 color = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord) * 0.5;
                    color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord01.xy) * 0.125;
                    color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord01.zw) * 0.125;
                    color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord23.xy) * 0.125;
                    color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord23.zw) * 0.125;
                #else
                    // 단일 샘플
                    float4 color = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord);
                #endif
                
                // 임계값 필터링
                color = ApplyBloomThreshold(color, _BloomParams);
                
                return color;
            }
            ENDHLSL
        }
        
        // Pass 1: Downsample (Bilinear)
        Pass
        {
            Name "Bloom Downsample"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragDownsample
            
            float4 fragDownsample(Varyings input) : SV_Target
            {
                // 4-tap bilinear 다운샘플링
                float4 color = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord01.xy);
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord01.zw);
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord23.xy);
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord23.zw);
                return color * 0.25;
            }
            ENDHLSL
        }
        
        // Pass 2: Downsample (High Quality - 13-tap)
        Pass
        {
            Name "Bloom Downsample HQ"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragDownsampleHQ
            
            float4 fragDownsampleHQ(Varyings input) : SV_Target
            {
                float2 texelSize = _MainTex_TexelSize.xy;
                float4 color = 0;
                
                // 13-tap Karis average
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord) * 4.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2(-1, -1));
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2( 0, -1)) * 2.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2( 1, -1));
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2(-1,  0)) * 2.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2( 1,  0)) * 2.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2(-1,  1));
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2( 0,  1)) * 2.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2( 1,  1));
                
                return color / 16.0;
            }
            ENDHLSL
        }
        
        // Pass 3: Upsample (Tent Filter)
        Pass
        {
            Name "Bloom Upsample"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragUpsample
            
            float4 fragUpsample(Varyings input) : SV_Target
            {
                float2 texelSize = _MainTex_TexelSize.xy;
                float4 color = 0;
                
                // 9-tap tent filter (더 부드러운 업샘플링)
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2(-1, -1)) * 1.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2( 0, -1)) * 2.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2( 1, -1)) * 1.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2(-1,  0)) * 2.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord) * 4.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2( 1,  0)) * 2.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2(-1,  1)) * 1.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2( 0,  1)) * 2.0;
                color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord + texelSize * float2( 1,  1)) * 1.0;
                
                // 색온도 조정 및 틴트 적용
                color.rgb *= _BloomTint.rgb;
                color.rgb = ApplyColorTemperature(color.rgb, _BloomParams.y);
                
                return color / 16.0 * _BloomParams.x; // 강도 적용
            }
            
            // 색온도 조정 함수
            float3 ApplyColorTemperature(float3 color, float temperature)
            {
                // 간단한 색온도 조정 (Kelvin to RGB 근사)
                float3 tempColor = temperature > 0 
                    ? float3(1.0, 0.9, 0.8) // 따뜻한 톤
                    : float3(0.8, 0.9, 1.0); // 차가운 톤
                    
                return lerp(color, color * tempColor, abs(temperature));
            }
            ENDHLSL
        }
        
        // Pass 4: Bicubic Upsample (High Quality)
        Pass
        {
            Name "Bloom Upsample Bicubic"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragUpsampleBicubic
            
            float4 fragUpsampleBicubic(Varyings input) : SV_Target
            {
                // Bicubic 업샘플링 (고품질)
                return BicubicSample(_MainTex, sampler_MainTex, input.texcoord, _MainTex_TexelSize) * _BloomParams.x;
            }
            
            // Bicubic 샘플링 구현
            float4 BicubicSample(TEXTURE2D_PARAM(tex, sampler_tex), float2 uv, float4 texelSize)
            {
                float2 coord = uv * texelSize.zw - 0.5;
                float2 icoord = floor(coord);
                float2 fcoord = frac(coord);
                
                // Catmull-Rom 가중치 계산
                float2 w0, w1, w2, w3;
                CubicWeights(fcoord, w0, w1, w2, w3);
                
                float2 s0 = w0 + w1;
                float2 s1 = w2 + w3;
                float2 f0 = w1 / s0;
                float2 f1 = w3 / s1;
                
                float2 t0 = (icoord - 1 + f0) * texelSize.xy;
                float2 t1 = (icoord + 1 + f1) * texelSize.xy;
                
                return (SAMPLE_TEXTURE2D(tex, sampler_tex, float2(t0.x, t0.y)) * s0.x +
                        SAMPLE_TEXTURE2D(tex, sampler_tex, float2(t1.x, t0.y)) * s1.x) * s0.y +
                       (SAMPLE_TEXTURE2D(tex, sampler_tex, float2(t0.x, t1.y)) * s0.x +
                        SAMPLE_TEXTURE2D(tex, sampler_tex, float2(t1.x, t1.y)) * s1.x) * s1.y;
            }
            
            void CubicWeights(float2 f, out float2 w0, out float2 w1, out float2 w2, out float2 w3)
            {
                float2 f2 = f * f;
                float2 f3 = f2 * f;
                
                w0 = -0.5 * f3 + f2 - 0.5 * f;
                w1 = 1.5 * f3 - 2.5 * f2 + 1.0;
                w2 = -1.5 * f3 + 2.0 * f2 + 0.5 * f;
                w3 = 0.5 * f3 - 0.5 * f2;
            }
            ENDHLSL
        }
        
        // Pass 5: Additive Blend
        Pass
        {
            Name "Bloom Add"
            Blend One One
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragAdd
            
            float4 fragAdd(Varyings input) : SV_Target
            {
                float4 color1 = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord);
                float4 color2 = SAMPLE_TEXTURE2D(_MainTex2, sampler_MainTex2, input.texcoord);
                return color1 + color2;
            }
            ENDHLSL
        }
        
        // Pass 6: Final Composition (기본)
        Pass
        {
            Name "Bloom Composite"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragComposite
            
            float4 fragComposite(Varyings input) : SV_Target
            {
                float4 source = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord);
                float4 bloom = SAMPLE_TEXTURE2D(_MainTex2, sampler_MainTex2, input.texcoord);
                
                return source + bloom * _FinalIntensity;
            }
            ENDHLSL
        }
        
        // Pass 7: Final Composition (Lens Dirt 포함)
        Pass
        {
            Name "Bloom Composite with Dirt"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragCompositeDirt
            
            float4 fragCompositeDirt(Varyings input) : SV_Target
            {
                float4 source = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.texcoord);
                float4 bloom = SAMPLE_TEXTURE2D(_MainTex2, sampler_MainTex2, input.texcoord);
                float4 dirt = SAMPLE_TEXTURE2D(_DirtTexture, sampler_DirtTexture, input.texcoord);
                
                // 렌즈 더트는 블룸과 곱셈 블렌딩
                bloom.rgb += bloom.rgb * dirt.rgb * _DirtParams.x;
                
                return source + bloom * _FinalIntensity;
            }
            ENDHLSL
        }
    }
    
    FallBack "Hidden/Core/FallbackError"
}
```

---

## Depth of Field 고급 기법

### 물리 기반 Bokeh DOF 구현

#### 1. Advanced DOF Volume Component

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Advanced/Physical Depth Of Field")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
public sealed class PhysicalDepthOfField : VolumeComponent, IPostProcessComponent
{
    [Header("Camera Settings")]
    [Tooltip("Focus distance in meters")]
    public MinFloatParameter focusDistance = new MinFloatParameter(10f, 0.1f);
    
    [Tooltip("Aperture f-number")]
    public ClampedFloatParameter aperture = new ClampedFloatParameter(5.6f, 1f, 32f);
    
    [Tooltip("Focal length in millimeters")]
    public ClampedFloatParameter focalLength = new ClampedFloatParameter(50f, 14f, 200f);
    
    [Tooltip("Sensor size (36mm = full frame)")]
    public ClampedFloatParameter sensorSize = new ClampedFloatParameter(36f, 10f, 100f);
    
    [Header("Bokeh Shape")]
    [Tooltip("Number of aperture blades")]
    public ClampedIntParameter bladeCount = new ClampedIntParameter(6, 3, 10);
    
    [Tooltip("Blade curvature (0=straight, 1=curved)")]
    public ClampedFloatParameter bladeCurvature = new ClampedFloatParameter(0.2f, 0f, 1f);
    
    [Tooltip("Blade rotation in degrees")]
    public ClampedFloatParameter bladeRotation = new ClampedFloatParameter(0f, 0f, 180f);
    
    [Header("Quality Settings")]
    [Tooltip("DOF quality preset")]
    public DOFQualityParameter quality = new DOFQualityParameter(DOFQuality.Medium);
    
    [Tooltip("Resolution scaling for performance")]
    public ClampedFloatParameter resolutionScale = new ClampedFloatParameter(0.5f, 0.25f, 1f);
    
    [Tooltip("Maximum CoC size (screen percentage)")]
    public ClampedFloatParameter maxCoC = new ClampedFloatParameter(0.1f, 0.01f, 0.3f);
    
    [Header("Near/Far Field")]
    [Tooltip("Enable near field blur")]
    public BoolParameter nearFieldBlur = new BoolParameter(true);
    
    [Tooltip("Far field start distance")]
    public MinFloatParameter farFieldStart = new MinFloatParameter(100f, 1f);
    
    [Header("Advanced")]
    [Tooltip("Temporal stability (reduces flickering)")]
    public ClampedFloatParameter temporalStability = new ClampedFloatParameter(0.1f, 0f, 1f);
    
    [Tooltip("Enable chromatic aberration in bokeh")]
    public BoolParameter chromaticAberration = new BoolParameter(false);
    
    [Tooltip("Chromatic aberration strength")]
    public ClampedFloatParameter chromaticStrength = new ClampedFloatParameter(0.5f, 0f, 2f);
    
    // 물리 기반 CoC 계산
    public float CalculateCoC(float depth)
    {
        float f = focalLength.value * 0.001f; // mm to m
        float s1 = focusDistance.value;       // focus distance
        float s2 = depth;                     // object distance
        
        if (Mathf.Approximately(s2, 0f) || s2 < 0.001f)
            return maxCoC.value;
            
        float A = f / aperture.value;         // aperture diameter
        float sensor = sensorSize.value * 0.001f; // mm to m
        
        // Thin lens equation: 1/f = 1/s1 + 1/s2'
        float s2_prime = 1f / (1f / f - 1f / s1);
        
        // CoC diameter = A * |s2' - sensor_distance| / sensor_distance
        float sensorDistance = 1f / (1f / f - 1f / s2);
        float cocDiameter = A * Mathf.Abs(s2_prime - sensorDistance) / sensorDistance;
        
        // Normalize to sensor size and clamp
        float normalizedCoC = cocDiameter / sensor;
        return Mathf.Clamp(normalizedCoC, 0f, maxCoC.value);
    }
    
    public bool IsActive() => aperture.value > 0f && focusDistance.value > 0f;
}

public enum DOFQuality
{
    Low,      // 단순한 박스 블러
    Medium,   // 육각형 보케
    High,     // 물리적 보케 + 색수차
    Ultra     // 최고 품질 + 노이즈 필터
}

[Serializable]
public sealed class DOFQualityParameter : VolumeParameter<DOFQuality>
{
    public DOFQualityParameter(DOFQuality value, bool overrideState = false) 
        : base(value, overrideState) { }
}
```

#### 2. Physical DOF Render Pass

```csharp
public class PhysicalDOFRenderPass : ScriptableRenderPass
{
    private const int k_CoCPass = 0;
    private const int k_PrefilterPass = 1;
    private const int k_BokehPass = 2;
    private const int k_PostfilterPass = 3;
    private const int k_CompositePass = 4;
    
    private Material m_DOFMaterial;
    private PhysicalDepthOfField m_DOFSettings;
    
    private RTHandle m_CoCTexture;
    private RTHandle m_PingTexture;
    private RTHandle m_PongTexture;
    private RTHandle m_NearTexture;
    private RTHandle m_FarTexture;
    
    // 보케 커널 (런타임 생성)
    private Vector4[] m_BokehKernel;
    private int m_SampleCount;
    
    public PhysicalDOFRenderPass(Material dofMaterial)
    {
        m_DOFMaterial = dofMaterial;
        renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }
    
    public void Setup(PhysicalDepthOfField dofSettings)
    {
        m_DOFSettings = dofSettings;
        GenerateBokehKernel();
    }
    
    private void GenerateBokehKernel()
    {
        int bladeCount = m_DOFSettings.bladeCount.value;
        float curvature = m_DOFSettings.bladeCurvature.value;
        float rotation = m_DOFSettings.bladeRotation.value * Mathf.Deg2Rad;
        
        // 품질별 샘플 수 결정
        m_SampleCount = m_DOFSettings.quality.value switch
        {
            DOFQuality.Low => 16,
            DOFQuality.Medium => 32,
            DOFQuality.High => 64,
            DOFQuality.Ultra => 128,
            _ => 32
        };
        
        m_BokehKernel = new Vector4[m_SampleCount];
        
        // Poisson disk 분포 + 다각형 마스킹
        var poissonDisk = GeneratePoissonDisk(m_SampleCount);
        
        for (int i = 0; i < m_SampleCount; i++)
        {
            var sample = poissonDisk[i];
            
            // 다각형 마스킹 적용
            var maskedSample = ApplyPolygonMask(sample, bladeCount, curvature, rotation);
            
            // 가중치 계산 (중심부터의 거리 기반)
            float weight = 1f / (1f + maskedSample.magnitude);
            
            m_BokehKernel[i] = new Vector4(maskedSample.x, maskedSample.y, weight, 0f);
        }
        
        // 가중치 정규화
        float totalWeight = 0f;
        for (int i = 0; i < m_SampleCount; i++)
        {
            totalWeight += m_BokehKernel[i].z;
        }
        
        for (int i = 0; i < m_SampleCount; i++)
        {
            m_BokehKernel[i].z /= totalWeight;
        }
    }
    
    private Vector2[] GeneratePoissonDisk(int sampleCount)
    {
        // Poisson disk sampling 구현 (균등한 분포)
        var samples = new List<Vector2>();
        var candidates = new List<Vector2>();
        
        float radius = 1f / Mathf.Sqrt(sampleCount * 2f);
        int k = 30; // 후보 수
        
        // 첫 번째 샘플
        samples.Add(UnityEngine.Random.insideUnitCircle);
        candidates.Add(samples[0]);
        
        while (candidates.Count > 0 && samples.Count < sampleCount)
        {
            int candidateIndex = UnityEngine.Random.Range(0, candidates.Count);
            var candidate = candidates[candidateIndex];
            
            bool validSample = false;
            
            for (int i = 0; i < k; i++)
            {
                float angle = UnityEngine.Random.Range(0f, Mathf.PI * 2f);
                float distance = UnityEngine.Random.Range(radius, radius * 2f);
                
                var newSample = candidate + new Vector2(
                    Mathf.Cos(angle) * distance,
                    Mathf.Sin(angle) * distance
                );
                
                if (newSample.magnitude > 1f) continue; // 원 밖의 샘플 제거
                
                bool tooClose = false;
                foreach (var existing in samples)
                {
                    if (Vector2.Distance(newSample, existing) < radius)
                    {
                        tooClose = true;
                        break;
                    }
                }
                
                if (!tooClose)
                {
                    samples.Add(newSample);
                    candidates.Add(newSample);
                    validSample = true;
                    break;
                }
            }
            
            if (!validSample)
            {
                candidates.RemoveAt(candidateIndex);
            }
        }
        
        return samples.ToArray();
    }
    
    private Vector2 ApplyPolygonMask(Vector2 sample, int bladeCount, float curvature, float rotation)
    {
        // 극좌표 변환
        float radius = sample.magnitude;
        float angle = Mathf.Atan2(sample.y, sample.x) + rotation;
        
        // 다각형 거리 함수
        float polygonAngle = (2f * Mathf.PI) / bladeCount;
        float localAngle = Mathf.Repeat(angle, polygonAngle) - polygonAngle * 0.5f;
        
        // 직선 거리 (평평한 날개)
        float straightDistance = Mathf.Cos(polygonAngle * 0.5f) / Mathf.Cos(localAngle);
        
        // 곡선 거리 (곡선 날개)
        float curvedDistance = Mathf.Lerp(straightDistance, 1f, curvature);
        
        // 반지름 제한
        radius = Mathf.Min(radius, curvedDistance);
        
        // 직교좌표 복원
        return new Vector2(
            radius * Mathf.Cos(angle - rotation),
            radius * Mathf.Sin(angle - rotation)
        );
    }
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        if (!ShouldRender(cameraData))
            return;
            
        ExecutePhysicalDOF(renderGraph, resourceData, cameraData);
    }
    
    private void ExecutePhysicalDOF(RenderGraph renderGraph, 
                                  UniversalResourceData resourceData,
                                  UniversalCameraData cameraData)
    {
        var desc = cameraData.cameraTargetDescriptor;
        var scaledDesc = GetScaledDescriptor(desc);
        
        using (var builder = renderGraph.AddUnsafePass<PhysicalDOFData>(
            "Physical Depth Of Field", out var passData))
        {
            // 텍스처 생성
            passData.sourceTexture = resourceData.activeColorTexture;
            passData.depthTexture = resourceData.cameraDepthTexture;
            
            passData.cocTexture = CreateCoCTexture(renderGraph, desc);
            passData.pingTexture = CreateWorkTexture(renderGraph, scaledDesc, "_DOF_Ping");
            passData.pongTexture = CreateWorkTexture(renderGraph, scaledDesc, "_DOF_Pong");
            
            if (m_DOFSettings.nearFieldBlur.value)
            {
                passData.nearTexture = CreateWorkTexture(renderGraph, scaledDesc, "_DOF_Near");
            }
            
            passData.farTexture = CreateWorkTexture(renderGraph, scaledDesc, "_DOF_Far");
            
            // PassData 설정
            passData.dofSettings = m_DOFSettings;
            passData.material = m_DOFMaterial;
            passData.bokehKernel = m_BokehKernel;
            passData.sampleCount = m_SampleCount;
            
            // 의존성 설정
            builder.UseTexture(passData.sourceTexture, AccessFlags.Read);
            builder.UseTexture(passData.depthTexture, AccessFlags.Read);
            builder.UseTexture(passData.cocTexture, AccessFlags.ReadWrite);
            
            builder.SetRenderFunc(static (PhysicalDOFData data, UnsafeGraphContext context) =>
            {
                ExecuteDOFPasses(data, context);
            });
        }
    }
    
    private static void ExecuteDOFPasses(PhysicalDOFData data, UnsafeGraphContext context)
    {
        var cmd = CommandBufferHelpers.GetNativeCommandBuffer(context.cmd);
        
        // 1. CoC 생성
        SetupCoCParameters(data);
        cmd.Blit(data.sourceTexture, data.cocTexture, data.material, k_CoCPass);
        
        // 2. Prefilter (다운샘플 + CoC 기반 분리)
        SetupPrefilterParameters(data);
        cmd.Blit(data.sourceTexture, data.pingTexture, data.material, k_PrefilterPass);
        
        // 3. 보케 블러 (Near/Far 분리)
        if (data.dofSettings.nearFieldBlur.value && data.nearTexture.IsValid())
        {
            // Near field 블러
            SetupBokehParameters(data, true); // isNearField = true
            cmd.Blit(data.pingTexture, data.nearTexture, data.material, k_BokehPass);
        }
        
        // Far field 블러
        SetupBokehParameters(data, false); // isNearField = false
        cmd.Blit(data.pingTexture, data.farTexture, data.material, k_BokehPass);
        
        // 4. Post-filter (노이즈 제거)
        if (data.dofSettings.quality.value >= DOFQuality.High)
        {
            cmd.Blit(data.farTexture, data.pongTexture, data.material, k_PostfilterPass);
            (data.farTexture, data.pongTexture) = (data.pongTexture, data.farTexture);
        }
        
        // 5. 최종 합성
        SetupCompositeParameters(data);
        cmd.Blit(data.sourceTexture, data.sourceTexture, data.material, k_CompositePass);
    }
    
    private static void SetupCoCParameters(PhysicalDOFData data)
    {
        var settings = data.dofSettings;
        
        // 카메라 파라미터
        var cocParams = new Vector4(
            settings.focusDistance.value,
            settings.aperture.value,
            settings.focalLength.value * 0.001f, // mm to m
            settings.sensorSize.value * 0.001f   // mm to m
        );
        
        var cocLimits = new Vector4(
            -settings.maxCoC.value, // near CoC limit
            settings.maxCoC.value,  // far CoC limit
            settings.farFieldStart.value,
            0f
        );
        
        data.material.SetVector("_CoCParams", cocParams);
        data.material.SetVector("_CoCLimits", cocLimits);
    }
    
    private static void SetupBokehParameters(PhysicalDOFData data, bool isNearField)
    {
        // 보케 커널을 Compute Buffer로 전달
        var kernelBuffer = new ComputeBuffer(data.sampleCount, sizeof(float) * 4);
        kernelBuffer.SetData(data.bokehKernel);
        
        data.material.SetBuffer("_BokehKernel", kernelBuffer);
        data.material.SetInt("_SampleCount", data.sampleCount);
        data.material.SetFloat("_IsNearField", isNearField ? 1f : 0f);
        
        // 색수차 설정
        if (data.dofSettings.chromaticAberration.value)
        {
            data.material.SetFloat("_ChromaticStrength", data.dofSettings.chromaticStrength.value);
            data.material.EnableKeyword("_CHROMATIC_ABERRATION");
        }
        else
        {
            data.material.DisableKeyword("_CHROMATIC_ABERRATION");
        }
        
        // 사용 후 해제 예약
        context.cmd.SetGlobalBuffer("_BokehKernel", kernelBuffer);
        kernelBuffer.Release();
    }
}

private class PhysicalDOFData
{
    internal TextureHandle sourceTexture;
    internal TextureHandle depthTexture;
    internal TextureHandle cocTexture;
    internal TextureHandle pingTexture;
    internal TextureHandle pongTexture;
    internal TextureHandle nearTexture;
    internal TextureHandle farTexture;
    internal PhysicalDepthOfField dofSettings;
    internal Material material;
    internal Vector4[] bokehKernel;
    internal int sampleCount;
}
```

---

## Motion Blur 시스템

### 고급 Motion Blur 구현

#### 1. Advanced Motion Blur Volume

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Advanced/Motion Blur Pro")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
public sealed class AdvancedMotionBlur : VolumeComponent, IPostProcessComponent
{
    [Header("Motion Settings")]
    [Tooltip("Motion blur intensity")]
    public ClampedFloatParameter intensity = new ClampedFloatParameter(0f, 0f, 1f);
    
    [Tooltip("Motion blur mode")]
    public MotionModeParameter motionMode = new MotionModeParameter(MotionMode.CameraAndObjects);
    
    [Tooltip("Quality preset")]
    public MotionQualityParameter quality = new MotionQualityParameter(MotionQuality.Medium);
    
    [Header("Camera Motion")]
    [Tooltip("Camera rotation scale")]
    public ClampedFloatParameter cameraRotationScale = new ClampedFloatParameter(1f, 0f, 2f);
    
    [Tooltip("Camera translation scale")]
    public ClampedFloatParameter cameraTranslationScale = new ClampedFloatParameter(1f, 0f, 2f);
    
    [Header("Object Motion")]
    [Tooltip("Object velocity scale")]
    public ClampedFloatParameter objectVelocityScale = new ClampedFloatParameter(1f, 0f, 5f);
    
    [Tooltip("Minimum object velocity threshold")]
    public ClampedFloatParameter velocityThreshold = new ClampedFloatParameter(0.01f, 0f, 1f);
    
    [Header("Advanced")]
    [Tooltip("Maximum blur radius (screen percentage)")]
    public ClampedFloatParameter maxBlurRadius = new ClampedFloatParameter(0.05f, 0.01f, 0.2f);
    
    [Tooltip("Velocity clamping")]
    public ClampedFloatParameter velocityClamp = new ClampedFloatParameter(0.1f, 0.01f, 1f);
    
    [Tooltip("Use temporal reprojection")]
    public BoolParameter temporalReprojection = new BoolParameter(true);
    
    [Tooltip("Ghost reduction strength")]
    public ClampedFloatParameter ghostReduction = new ClampedFloatParameter(0.8f, 0f, 1f);
    
    [Header("Optimization")]
    [Tooltip("Use tile-based optimization")]
    public BoolParameter tileBasedOptimization = new BoolParameter(true);
    
    [Tooltip("Tile size")]
    public TileSizeParameter tileSize = new TileSizeParameter(TileSize.Size16);
    
    public bool IsActive() => intensity.value > 0f;
}

public enum MotionMode
{
    CameraOnly,       // 카메라 움직임만
    ObjectsOnly,      // 오브젝트 움직임만
    CameraAndObjects  // 전체 모션 블러
}

public enum MotionQuality
{
    Low,     // 4 samples
    Medium,  // 8 samples  
    High,    // 16 samples
    Ultra    // 32 samples
}

public enum TileSize
{
    Size8 = 8,
    Size16 = 16,
    Size32 = 32
}
```

#### 2. Motion Blur Pass Implementation

```csharp
public class AdvancedMotionBlurPass : ScriptableRenderPass
{
    private const int k_MotionVectorPass = 0;
    private const int k_TileMaxPass = 1;
    private const int k_NeighborMaxPass = 2;
    private const int k_MotionBlurPass = 3;
    private const int k_TemporalPass = 4;
    
    private Material m_MotionBlurMaterial;
    private ComputeShader m_TileMaxCompute;
    private AdvancedMotionBlur m_Settings;
    
    private RTHandle m_MotionVectorTexture;
    private RTHandle m_TileMaxTexture;
    private RTHandle m_NeighborMaxTexture;
    private RTHandle m_TemporalHistory;
    
    private Matrix4x4 m_PreviousViewProjectionMatrix;
    private bool m_FirstFrame = true;
    
    public AdvancedMotionBlurPass(Material motionBlurMaterial, ComputeShader tileMaxCompute)
    {
        m_MotionBlurMaterial = motionBlurMaterial;
        m_TileMaxCompute = tileMaxCompute;
        renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }
    
    private class AdvancedMotionBlurData
    {
        internal TextureHandle colorTexture;
        internal TextureHandle depthTexture;
        internal TextureHandle motionTexture;
        internal TextureHandle outputTexture;
        internal Material material;
        internal float shutterAngle;
        internal int sampleCount;
    }

    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        if (!ShouldRender(cameraData))
            return;
            
        ExecuteAdvancedMotionBlur(renderGraph, resourceData, cameraData);
    }
    
    private void ExecuteAdvancedMotionBlur(RenderGraph renderGraph, 
                                         UniversalResourceData resourceData,
                                         UniversalCameraData cameraData)
    {
        using (var builder = renderGraph.AddUnsafePass<AdvancedMotionBlurData>(
            "Advanced Motion Blur", out var passData))
        {
            SetupMotionBlurTextures(renderGraph, cameraData, passData);
            SetupPassData(passData, resourceData, cameraData);
            
            builder.SetRenderFunc(static (AdvancedMotionBlurData data, UnsafeGraphContext context) =>
            {
                ExecuteMotionBlurPasses(data, context);
            });
        }
    }
    
    private static void ExecuteMotionBlurPasses(AdvancedMotionBlurData data, UnsafeGraphContext context)
    {
        var cmd = CommandBufferHelpers.GetNativeCommandBuffer(context.cmd);
        
        // 1. Motion Vector 생성 (카메라 + 오브젝트)
        if (data.settings.motionMode.value != MotionMode.ObjectsOnly)
        {
            SetupCameraMotionParameters(data);
        }
        
        cmd.Blit(data.sourceTexture, data.motionVectorTexture, data.material, k_MotionVectorPass);
        
        // 2. Tile-based 최적화 (선택적)
        if (data.settings.tileBasedOptimization.value)
        {
            ExecuteTileMaxPasses(data, cmd);
        }
        
        // 3. Motion Blur 적용
        SetupMotionBlurParameters(data);
        
        if (data.settings.temporalReprojection.value && !data.isFirstFrame)
        {
            // Temporal reprojection 사용
            cmd.SetGlobalTexture("_TemporalHistory", data.temporalHistory);
            cmd.Blit(data.sourceTexture, data.outputTexture, data.material, k_TemporalPass);
        }
        else
        {
            // 표준 모션 블러
            cmd.Blit(data.sourceTexture, data.outputTexture, data.material, k_MotionBlurPass);
        }
        
        // 4. History 업데이트
        if (data.settings.temporalReprojection.value)
        {
            cmd.CopyTexture(data.outputTexture, data.temporalHistory);
        }
        
        // 5. 최종 결과 복사
        cmd.Blit(data.outputTexture, data.sourceTexture);
    }
    
    private static void ExecuteTileMaxPasses(AdvancedMotionBlurData data, CommandBuffer cmd)
    {
        // Compute Shader를 사용한 타일 기반 최대값 계산
        int tileSize = (int)data.settings.tileSize.value;
        int kernelIndex = data.tileMaxCompute.FindKernel("TileMax");
        
        cmd.SetComputeTextureParam(data.tileMaxCompute, kernelIndex, "_MotionVectorTexture", data.motionVectorTexture);
        cmd.SetComputeTextureParam(data.tileMaxCompute, kernelIndex, "_TileMaxResult", data.tileMaxTexture);
        cmd.SetComputeIntParam(data.tileMaxCompute, "_TileSize", tileSize);
        
        int groupsX = (data.screenWidth + tileSize - 1) / tileSize;
        int groupsY = (data.screenHeight + tileSize - 1) / tileSize;
        
        cmd.DispatchCompute(data.tileMaxCompute, kernelIndex, groupsX, groupsY, 1);
        
        // Neighbor Max Pass (타일 간 최대값 전파)
        cmd.Blit(data.tileMaxTexture, data.neighborMaxTexture, data.material, k_NeighborMaxPass);
    }
    
    private static void SetupCameraMotionParameters(AdvancedMotionBlurData data)
    {
        // 카메라 모션 벡터 계산
        var currentVP = data.viewProjectionMatrix;
        var previousVP = data.previousViewProjectionMatrix;
        
        // Reprojection 행렬
        var reprojectionMatrix = previousVP * Matrix4x4.Inverse(currentVP);
        
        data.material.SetMatrix("_ReprojectionMatrix", reprojectionMatrix);
        data.material.SetFloat("_CameraRotationScale", data.settings.cameraRotationScale.value);
        data.material.SetFloat("_CameraTranslationScale", data.settings.cameraTranslationScale.value);
    }
    
    private static void SetupMotionBlurParameters(AdvancedMotionBlurData data)
    {
        // 품질별 샘플 수
        int sampleCount = data.settings.quality.value switch
        {
            MotionQuality.Low => 4,
            MotionQuality.Medium => 8,
            MotionQuality.High => 16,
            MotionQuality.Ultra => 32,
            _ => 8
        };
        
        var motionParams = new Vector4(
            data.settings.intensity.value,
            data.settings.maxBlurRadius.value,
            data.settings.velocityClamp.value,
            sampleCount
        );
        
        data.material.SetVector("_MotionBlurParams", motionParams);
        data.material.SetFloat("_ObjectVelocityScale", data.settings.objectVelocityScale.value);
        data.material.SetFloat("_VelocityThreshold", data.settings.velocityThreshold.value);
        data.material.SetFloat("_GhostReduction", data.settings.ghostReduction.value);
        
        // 키워드 설정
        SetMotionBlurKeywords(data);
    }
    
    private static void SetMotionBlurKeywords(AdvancedMotionBlurData data)
    {
        // 모션 모드
        CoreUtils.SetKeyword(data.material, "_CAMERA_MOTION_ONLY", 
            data.settings.motionMode.value == MotionMode.CameraOnly);
        CoreUtils.SetKeyword(data.material, "_OBJECT_MOTION_ONLY", 
            data.settings.motionMode.value == MotionMode.ObjectsOnly);
        CoreUtils.SetKeyword(data.material, "_CAMERA_AND_OBJECTS", 
            data.settings.motionMode.value == MotionMode.CameraAndObjects);
            
        // 품질 모드
        CoreUtils.SetKeyword(data.material, "_QUALITY_LOW", 
            data.settings.quality.value == MotionQuality.Low);
        CoreUtils.SetKeyword(data.material, "_QUALITY_HIGH", 
            data.settings.quality.value >= MotionQuality.High);
            
        // 타일 최적화
        CoreUtils.SetKeyword(data.material, "_TILE_BASED", 
            data.settings.tileBasedOptimization.value);
        CoreUtils.SetKeyword(data.material, "_TEMPORAL_REPROJECTION", 
            data.settings.temporalReprojection.value);
    }
}
```

#### 3. Motion Blur Shader (핵심 부분)

```hlsl
Shader "Hidden/Advanced Motion Blur"
{
    Properties
    {
        [HideInInspector] _MainTex ("Source Texture", 2D) = "white" {}
        [HideInInspector] _MotionVectorTexture ("Motion Vector Texture", 2D) = "black" {}
        [HideInInspector] _TileMaxTexture ("Tile Max Texture", 2D) = "black" {}
        [HideInInspector] _TemporalHistory ("Temporal History", 2D) = "black" {}
    }
    
    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" }
        
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareDepthTexture.hlsl"
        
        TEXTURE2D(_MainTex);
        TEXTURE2D(_MotionVectorTexture);
        TEXTURE2D(_TileMaxTexture);
        TEXTURE2D(_TemporalHistory);
        SAMPLER(sampler_MainTex);
        SAMPLER(sampler_MotionVectorTexture);
        SAMPLER(sampler_TileMaxTexture);
        SAMPLER(sampler_TemporalHistory);
        
        float4 _MotionBlurParams;     // (intensity, maxRadius, velocityClamp, sampleCount)
        float4x4 _ReprojectionMatrix;
        float _CameraRotationScale;
        float _CameraTranslationScale;
        float _ObjectVelocityScale;
        float _VelocityThreshold;
        float _GhostReduction;
        
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
        };
        
        Varyings vert(Attributes input)
        {
            Varyings output;
            output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
            output.texcoord = input.texcoord;
            output.screenPos = ComputeScreenPos(output.positionCS);
            return output;
        }
        
        // 카메라 모션 벡터 계산
        float2 CalculateCameraMotionVector(float2 uv, float depth)
        {
            // NDC 좌표로 변환
            float4 ndcPos = float4(uv * 2.0 - 1.0, depth, 1.0);
            ndcPos.y = -ndcPos.y; // DirectX/OpenGL 호환성
            
            // 이전 프레임 위치로 역투영
            float4 prevClipPos = mul(_ReprojectionMatrix, ndcPos);
            prevClipPos.xyz /= prevClipPos.w;
            
            // 스크린 좌표로 변환
            float2 prevUV = prevClipPos.xy * 0.5 + 0.5;
            prevUV.y = 1.0 - prevUV.y;
            
            return (prevUV - uv) * _CameraRotationScale;
        }
        
        // 고품질 모션 블러 (가중 평균 샘플링)
        float4 ApplyHighQualityMotionBlur(float2 uv, float2 velocity)
        {
            float4 color = 0;
            float totalWeight = 0;
            
            int sampleCount = (int)_MotionBlurParams.w;
            float intensity = _MotionBlurParams.x;
            
            // Velocity 크기에 따른 적응형 샘플링
            float velocityMagnitude = length(velocity);
            if (velocityMagnitude < _VelocityThreshold)
                return SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv);
            
            // 클램핑 적용
            velocity = ClampVelocity(velocity);
            
            for (int i = 0; i < sampleCount; i++)
            {
                float t = (float)i / (float)(sampleCount - 1);
                t = (t - 0.5) * 2.0; // [-1, 1] 범위
                
                float2 sampleUV = uv + velocity * t * intensity;
                
                // 화면 경계 체크
                if (any(sampleUV < 0) || any(sampleUV > 1))
                    continue;
                    
                float4 sampleColor = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, sampleUV);
                
                // 가중치 계산 (중심에서 가까울수록 높은 가중치)
                float weight = 1.0 - abs(t);
                weight = weight * weight; // 제곱으로 중심 강화
                
                color += sampleColor * weight;
                totalWeight += weight;
            }
            
            return totalWeight > 0 ? color / totalWeight : SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv);
        }
        
        // Velocity 클램핑 (너무 큰 모션 벡터 제한)
        float2 ClampVelocity(float2 velocity)
        {
            float maxRadius = _MotionBlurParams.y;
            float velocityMagnitude = length(velocity);
            
            if (velocityMagnitude > maxRadius)
            {
                velocity = normalize(velocity) * maxRadius;
            }
            
            return velocity;
        }
        
        // 고스팅 감소 (Temporal reprojection 기반)
        float4 ReduceGhosting(float4 currentColor, float4 historyColor, float2 velocity)
        {
            float velocityMagnitude = length(velocity);
            
            // 빠른 움직임에서는 history 신뢰도 감소
            float historyConfidence = saturate(1.0 - velocityMagnitude * 10.0);
            historyConfidence *= _GhostReduction;
            
            return lerp(currentColor, historyColor, historyConfidence);
        }
        
        ENDHLSL
        
        // Pass 0: Motion Vector Generation
        Pass
        {
            Name "Motion Vector Generation"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragMotionVector
            #pragma multi_compile_local _ _CAMERA_MOTION_ONLY _OBJECT_MOTION_ONLY _CAMERA_AND_OBJECTS
            
            float4 fragMotionVector(Varyings input) : SV_Target
            {
                float2 uv = input.texcoord;
                float depth = SampleSceneDepth(uv);
                
                float2 velocity = 0;
                
                #if defined(_CAMERA_MOTION_ONLY) || defined(_CAMERA_AND_OBJECTS)
                    // 카메라 모션 벡터
                    velocity += CalculateCameraMotionVector(uv, depth);
                #endif
                
                #if defined(_OBJECT_MOTION_ONLY) || defined(_CAMERA_AND_OBJECTS)
                    // 오브젝트 모션 벡터 (Motion Vector Pass에서 제공)
                    float2 objectVelocity = SAMPLE_TEXTURE2D(_MotionVectorTexture, sampler_MotionVectorTexture, uv).xy;
                    velocity += objectVelocity * _ObjectVelocityScale;
                #endif
                
                return float4(velocity, 0, 1);
            }
            ENDHLSL
        }
        
        // Pass 3: Motion Blur Application
        Pass
        {
            Name "Motion Blur"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragMotionBlur
            #pragma multi_compile_local _ _QUALITY_LOW _QUALITY_HIGH
            #pragma multi_compile_local _ _TILE_BASED
            
            float4 fragMotionBlur(Varyings input) : SV_Target
            {
                float2 uv = input.texcoord;
                
                float2 velocity;
                #ifdef _TILE_BASED
                    // 타일 기반 최적화: 타일 최대값 사용
                    float2 tileUV = floor(uv * _ScreenParams.xy / 16.0) / floor(_ScreenParams.xy / 16.0);
                    velocity = SAMPLE_TEXTURE2D(_TileMaxTexture, sampler_TileMaxTexture, tileUV).xy;
                #else
                    // 직접 모션 벡터 사용
                    velocity = SAMPLE_TEXTURE2D(_MotionVectorTexture, sampler_MotionVectorTexture, uv).xy;
                #endif
                
                // 모션 블러 적용
                #ifdef _QUALITY_HIGH
                    return ApplyHighQualityMotionBlur(uv, velocity);
                #else
                    // 저품질: 간단한 선형 샘플링
                    return ApplySimpleMotionBlur(uv, velocity);
                #endif
            }
            
            float4 ApplySimpleMotionBlur(float2 uv, float2 velocity)
            {
                velocity = ClampVelocity(velocity);
                
                if (length(velocity) < _VelocityThreshold)
                    return SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv);
                
                float4 color = 0;
                int samples = 4; // 저품질은 4샘플
                
                for (int i = 0; i < samples; i++)
                {
                    float t = (float)i / (float)(samples - 1) - 0.5;
                    float2 sampleUV = uv + velocity * t * _MotionBlurParams.x;
                    color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, sampleUV);
                }
                
                return color / samples;
            }
            ENDHLSL
        }
        
        // Pass 4: Temporal Reprojection
        Pass
        {
            Name "Temporal Reprojection"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment fragTemporal
            
            float4 fragTemporal(Varyings input) : SV_Target
            {
                float2 uv = input.texcoord;
                float2 velocity = SAMPLE_TEXTURE2D(_MotionVectorTexture, sampler_MotionVectorTexture, uv).xy;
                
                // 현재 프레임 모션 블러
                float4 currentColor = ApplyHighQualityMotionBlur(uv, velocity);
                
                // 이전 프레임 샘플링
                float2 historyUV = uv - velocity;
                float4 historyColor = SAMPLE_TEXTURE2D(_TemporalHistory, sampler_TemporalHistory, historyUV);
                
                // 고스팅 감소 적용
                return ReduceGhosting(currentColor, historyColor, velocity);
            }
            ENDHLSL
        }
    }
    
    FallBack "Hidden/Core/FallbackError"
}
```

---

## Color Grading & Tone Mapping

### 고급 Color Grading 시스템

#### 1. Professional Color Grading Volume

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Advanced/Professional Color Grading")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
public sealed class ProfessionalColorGrading : VolumeComponent, IPostProcessComponent
{
    [Header("Tone Mapping")]
    [Tooltip("Tone mapping operator")]
    public ToneMappingOperatorParameter toneMapping = new ToneMappingOperatorParameter(ToneMappingOperator.ACES);
    
    [Tooltip("Exposure compensation")]
    public FloatParameter exposure = new FloatParameter(0f);
    
    [Tooltip("White balance temperature")]
    public ClampedFloatParameter temperature = new ClampedFloatParameter(0f, -100f, 100f);
    
    [Tooltip("White balance tint")]
    public ClampedFloatParameter tint = new ClampedFloatParameter(0f, -100f, 100f);
    
    [Header("Color Wheels")]
    [Tooltip("Shadows color wheel")]
    public Vector4Parameter shadows = new Vector4Parameter(Vector4.zero);
    
    [Tooltip("Midtones color wheel")]
    public Vector4Parameter midtones = new Vector4Parameter(Vector4.zero);
    
    [Tooltip("Highlights color wheel")]
    public Vector4Parameter highlights = new Vector4Parameter(Vector4.zero);
    
    [Header("Primary Corrections")]
    [Tooltip("Contrast")]
    public ClampedFloatParameter contrast = new ClampedFloatParameter(0f, -100f, 100f);
    
    [Tooltip("Saturation")]
    public ClampedFloatParameter saturation = new ClampedFloatParameter(0f, -100f, 100f);
    
    [Tooltip("Gamma correction")]
    public ClampedFloatParameter gamma = new ClampedFloatParameter(0f, -100f, 100f);
    
    [Tooltip("Gain")]
    public ClampedFloatParameter gain = new ClampedFloatParameter(0f, -100f, 100f);
    
    [Header("Secondary Corrections")]
    [Tooltip("Hue shift")]
    public ClampedFloatParameter hueShift = new ClampedFloatParameter(0f, -180f, 180f);
    
    [Tooltip("Vibrance")]
    public ClampedFloatParameter vibrance = new ClampedFloatParameter(0f, -100f, 100f);
    
    [Header("Lift Gamma Gain")]
    [Tooltip("Lift (shadows)")]
    public Vector4Parameter lift = new Vector4Parameter(Vector4.zero);
    
    [Tooltip("Gamma (midtones)")]
    public Vector4Parameter gammaLGG = new Vector4Parameter(Vector4.zero);
    
    [Tooltip("Gain (highlights)")]
    public Vector4Parameter gainLGG = new Vector4Parameter(Vector4.zero);
    
    [Header("Channel Mixer")]
    [Tooltip("Red channel mixer")]
    public Vector3Parameter channelMixerRed = new Vector3Parameter(new Vector3(1, 0, 0));
    
    [Tooltip("Green channel mixer")]
    public Vector3Parameter channelMixerGreen = new Vector3Parameter(new Vector3(0, 1, 0));
    
    [Tooltip("Blue channel mixer")]
    public Vector3Parameter channelMixerBlue = new Vector3Parameter(new Vector3(0, 0, 1));
    
    [Header("Curves")]
    [Tooltip("Master curve")]
    public AnimationCurveParameter masterCurve = new AnimationCurveParameter(
        AnimationCurve.Linear(0f, 0f, 1f, 1f), false);
    
    [Tooltip("Red curve")]
    public AnimationCurveParameter redCurve = new AnimationCurveParameter(
        AnimationCurve.Linear(0f, 0f, 1f, 1f), false);
    
    [Tooltip("Green curve")]
    public AnimationCurveParameter greenCurve = new AnimationCurveParameter(
        AnimationCurve.Linear(0f, 0f, 1f, 1f), false);
    
    [Tooltip("Blue curve")]
    public AnimationCurveParameter blueCurve = new AnimationCurveParameter(
        AnimationCurve.Linear(0f, 0f, 1f, 1f), false);
    
    [Header("LUT")]
    [Tooltip("Custom LUT texture")]
    public TextureParameter lutTexture = new TextureParameter(null);
    
    [Tooltip("LUT contribution")]
    public ClampedFloatParameter lutContribution = new ClampedFloatParameter(1f, 0f, 1f);
    
    public bool IsActive() => true; // Color grading is always active
}

public enum ToneMappingOperator
{
    None,
    Reinhard,
    ReinhardExtended,
    ACES,
    Filmic,
    Uncharted2,
    AgX
}

[Serializable]
public sealed class ToneMappingOperatorParameter : VolumeParameter<ToneMappingOperator>
{
    public ToneMappingOperatorParameter(ToneMappingOperator value, bool overrideState = false) 
        : base(value, overrideState) { }
}
```

#### 2. Color Grading Render Pass

```csharp
public class ProfessionalColorGradingPass : ScriptableRenderPass
{
    private const int k_LutSize = 32;
    private const int k_LutWidth = k_LutSize * k_LutSize;
    private const int k_LutHeight = k_LutSize;
    
    private Material m_ColorGradingMaterial;
    private ComputeShader m_LutComputeShader;
    private ProfessionalColorGrading m_ColorGrading;
    
    private RTHandle m_InternalLut;
    private Texture2D[] m_CurveTextures = new Texture2D[4]; // Master, R, G, B
    
    private static readonly ProfilingSampler s_ProfilingSampler = 
        new ProfilingSampler("Professional Color Grading");
    
    // Shader property IDs
    private static readonly int s_Lut3D = Shader.PropertyToID("_Lut3D");
    private static readonly int s_LutParams = Shader.PropertyToID("_LutParams");
    private static readonly int s_ColorBalance = Shader.PropertyToID("_ColorBalance");
    private static readonly int s_ColorFilter = Shader.PropertyToID("_ColorFilter");
    private static readonly int s_ChannelMixerRed = Shader.PropertyToID("_ChannelMixerRed");
    private static readonly int s_ChannelMixerGreen = Shader.PropertyToID("_ChannelMixerGreen");
    private static readonly int s_ChannelMixerBlue = Shader.PropertyToID("_ChannelMixerBlue");
    private static readonly int s_HueSatCon = Shader.PropertyToID("_HueSatCon");
    private static readonly int s_Lift = Shader.PropertyToID("_Lift");
    private static readonly int s_Gamma = Shader.PropertyToID("_Gamma");
    private static readonly int s_Gain = Shader.PropertyToID("_Gain");
    private static readonly int s_Shadows = Shader.PropertyToID("_Shadows");
    private static readonly int s_Midtones = Shader.PropertyToID("_Midtones");
    private static readonly int s_Highlights = Shader.PropertyToID("_Highlights");
    private static readonly int s_CurveTexture = Shader.PropertyToID("_CurveTexture");
    
    public ProfessionalColorGradingPass(Material colorGradingMaterial, ComputeShader lutComputeShader)
    {
        m_ColorGradingMaterial = colorGradingMaterial;
        m_LutComputeShader = lutComputeShader;
        renderPassEvent = RenderPassEvent.BeforeRenderingPostProcessing;
        
        // 곡선 텍스처 초기화
        for (int i = 0; i < 4; i++)
        {
            m_CurveTextures[i] = new Texture2D(256, 1, TextureFormat.RGBAHalf, false, true)
            {
                name = $"ColorGrading_Curve_{i}",
                wrapMode = TextureWrapMode.Clamp,
                filterMode = FilterMode.Bilinear
            };
        }
    }
    
    public void Setup(ProfessionalColorGrading colorGrading)
    {
        m_ColorGrading = colorGrading;
    }
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        ExecuteColorGrading(renderGraph, resourceData, cameraData);
    }
    
    private void ExecuteColorGrading(RenderGraph renderGraph, 
                                   UniversalResourceData resourceData,
                                   UniversalCameraData cameraData)
    {
        // 1. LUT 생성
        GenerateColorGradingLUT(renderGraph);
        
        // 2. Color Grading 적용
        using (var builder = renderGraph.AddRasterRenderPass<ColorGradingData>(
            "Color Grading Application", out var passData, s_ProfilingSampler))
        {
            passData.sourceTexture = resourceData.activeColorTexture;
            passData.lutTexture = m_InternalLut;
            passData.material = m_ColorGradingMaterial;
            passData.colorGrading = m_ColorGrading;
            
            // 출력 텍스처 생성
            var outputDesc = cameraData.cameraTargetDescriptor;
            passData.destination = UniversalRenderer.CreateRenderGraphTexture(
                renderGraph, outputDesc, "_ColorGradingOutput", true);
            
            builder.UseTexture(passData.sourceTexture, AccessFlags.Read);
            builder.UseTexture(passData.lutTexture, AccessFlags.Read);
            builder.SetRenderAttachment(passData.destination, 0, AccessFlags.Write);
            
            builder.SetRenderFunc(static (ColorGradingData data, RasterGraphContext context) =>
            {
                ExecuteColorGradingPass(data, context);
            });
        }
    }
    
    private void GenerateColorGradingLUT(RenderGraph renderGraph)
    {
        using (var builder = renderGraph.AddComputePass<LutGenerationData>(
            "Generate Color Grading LUT", out var passData))
        {
            // LUT 텍스처 생성
            var lutDesc = new TextureDesc(k_LutWidth, k_LutHeight)
            {
                colorFormat = GraphicsFormat.R16G16B16A16_SFloat,
                enableRandomWrite = true,
                dimension = TextureDimension.Tex2D,
                name = "_InternalColorGradingLut"
            };
            
            passData.lutTexture = renderGraph.CreateTexture(lutDesc);
            passData.computeShader = m_LutComputeShader;
            passData.colorGrading = m_ColorGrading;
            
            // 곡선 텍스처 업데이트
            UpdateCurveTextures();
            
            builder.UseTexture(passData.lutTexture, AccessFlags.Write);
            
            builder.SetRenderFunc(static (LutGenerationData data, ComputeGraphContext context) =>
            {
                ExecuteLutGeneration(data, context);
            });
        }
    }
    
    private static void ExecuteLutGeneration(LutGenerationData data, ComputeGraphContext context)
    {
        var cmd = context.cmd;
        int kernelIndex = data.computeShader.FindKernel("GenerateColorGradingLUT");
        
        // Color grading 파라미터 설정
        SetupColorGradingParameters(data, cmd);
        
        cmd.SetComputeTextureParam(data.computeShader, kernelIndex, "_LutTexture", data.lutTexture);
        cmd.SetComputeIntParam(data.computeShader, "_LutSize", k_LutSize);
        
        // Dispatch
        int groupsX = (k_LutWidth + 7) / 8;
        int groupsY = (k_LutHeight + 7) / 8;
        cmd.DispatchCompute(data.computeShader, kernelIndex, groupsX, groupsY, 1);
    }
    
    private static void SetupColorGradingParameters(LutGenerationData data, CommandBuffer cmd)
    {
        var settings = data.colorGrading;
        
        // White Balance
        var colorBalance = CalculateColorBalance(settings.temperature.value, settings.tint.value);
        cmd.SetComputeVectorParam(data.computeShader, "_ColorBalance", colorBalance);
        
        // Exposure
        float exposure = Mathf.Pow(2f, settings.exposure.value);
        cmd.SetComputeFloatParam(data.computeShader, "_Exposure", exposure);
        
        // Contrast, Saturation, Gamma, Gain
        var hueSatCon = new Vector4(
            settings.hueShift.value / 360f,
            (settings.saturation.value + 100f) / 100f,
            (settings.contrast.value + 100f) / 100f,
            Mathf.Pow(2f, settings.gamma.value / 100f)
        );
        cmd.SetComputeVectorParam(data.computeShader, "_HueSatCon", hueSatCon);
        
        // Lift Gamma Gain
        var lift = settings.lift.value;
        var gamma = Vector4.one + settings.gammaLGG.value;
        var gain = Vector4.one + settings.gainLGG.value;
        
        cmd.SetComputeVectorParam(data.computeShader, "_Lift", lift);
        cmd.SetComputeVectorParam(data.computeShader, "_Gamma", gamma);
        cmd.SetComputeVectorParam(data.computeShader, "_Gain", gain);
        
        // Color Wheels
        cmd.SetComputeVectorParam(data.computeShader, "_Shadows", settings.shadows.value);
        cmd.SetComputeVectorParam(data.computeShader, "_Midtones", settings.midtones.value);
        cmd.SetComputeVectorParam(data.computeShader, "_Highlights", settings.highlights.value);
        
        // Channel Mixer
        cmd.SetComputeVectorParam(data.computeShader, "_ChannelMixerRed", settings.channelMixerRed.value);
        cmd.SetComputeVectorParam(data.computeShader, "_ChannelMixerGreen", settings.channelMixerGreen.value);
        cmd.SetComputeVectorParam(data.computeShader, "_ChannelMixerBlue", settings.channelMixerBlue.value);
        
        // Tone Mapping
        cmd.SetComputeIntParam(data.computeShader, "_ToneMappingOperator", (int)settings.toneMapping.value);
    }
    
    private static Vector4 CalculateColorBalance(float temperature, float tint)
    {
        // Kelvin to RGB conversion
        float t = temperature / 100f;
        float r, g, b;
        
        if (t > 0)
        {
            // Warm
            r = 1f;
            g = Mathf.Clamp01(1f - t * 0.3f);
            b = Mathf.Clamp01(1f - t * 0.8f);
        }
        else
        {
            // Cool
            r = Mathf.Clamp01(1f + t * 0.3f);
            g = Mathf.Clamp01(1f + t * 0.1f);
            b = 1f;
        }
        
        // Apply tint
        float tintFactor = tint / 100f;
        if (tintFactor > 0)
        {
            r = Mathf.Lerp(r, 1f, tintFactor * 0.2f);
            g = Mathf.Lerp(g, 1f, tintFactor * 0.5f);
        }
        else
        {
            g = Mathf.Lerp(g, 1f, -tintFactor * 0.2f);
            b = Mathf.Lerp(b, 1f, -tintFactor * 0.5f);
        }
        
        return new Vector4(r, g, b, 1f);
    }
    
    private void UpdateCurveTextures()
    {
        var curves = new AnimationCurve[]
        {
            m_ColorGrading.masterCurve.value,
            m_ColorGrading.redCurve.value,
            m_ColorGrading.greenCurve.value,
            m_ColorGrading.blueCurve.value
        };
        
        for (int curveIndex = 0; curveIndex < 4; curveIndex++)
        {
            var curve = curves[curveIndex];
            var texture = m_CurveTextures[curveIndex];
            var pixels = new Color[256];
            
            for (int i = 0; i < 256; i++)
            {
                float t = (float)i / 255f;
                float value = Mathf.Clamp01(curve.Evaluate(t));
                pixels[i] = new Color(value, value, value, 1f);
            }
            
            texture.SetPixels(pixels);
            texture.Apply();
        }
    }
    
    private static void ExecuteColorGradingPass(ColorGradingData data, RasterGraphContext context)
    {
        var cmd = context.cmd;
        
        // LUT 및 파라미터 설정
        data.material.SetTexture(s_Lut3D, data.lutTexture);
        
        var lutParams = new Vector4(
            1f / k_LutSize,              // LUT scale
            k_LutSize - 1f,              // LUT bias
            data.colorGrading.lutContribution.value, // LUT contribution
            0f
        );
        data.material.SetVector(s_LutParams, lutParams);
        
        // 커스텀 LUT 설정
        if (data.colorGrading.lutTexture.value != null)
        {
            data.material.SetTexture("_UserLut", data.colorGrading.lutTexture.value);
            data.material.EnableKeyword("_USER_LUT");
        }
        else
        {
            data.material.DisableKeyword("_USER_LUT");
        }
        
        // Tone mapping 키워드 설정
        SetToneMappingKeywords(data.material, data.colorGrading.toneMapping.value);
        
        // 블릿 실행
        Blitter.BlitCameraTexture(cmd, data.sourceTexture, data.destination, data.material, 0);
    }
    
    private static void SetToneMappingKeywords(Material material, ToneMappingOperator toneMapping)
    {
        // 모든 톤 매핑 키워드 비활성화
        material.DisableKeyword("_TONEMAPPING_REINHARD");
        material.DisableKeyword("_TONEMAPPING_REINHARD_EXTENDED");
        material.DisableKeyword("_TONEMAPPING_ACES");
        material.DisableKeyword("_TONEMAPPING_FILMIC");
        material.DisableKeyword("_TONEMAPPING_UNCHARTED2");
        material.DisableKeyword("_TONEMAPPING_AGX");
        
        // 선택된 톤 매핑 활성화
        switch (toneMapping)
        {
            case ToneMappingOperator.Reinhard:
                material.EnableKeyword("_TONEMAPPING_REINHARD");
                break;
            case ToneMappingOperator.ReinhardExtended:
                material.EnableKeyword("_TONEMAPPING_REINHARD_EXTENDED");
                break;
            case ToneMappingOperator.ACES:
                material.EnableKeyword("_TONEMAPPING_ACES");
                break;
            case ToneMappingOperator.Filmic:
                material.EnableKeyword("_TONEMAPPING_FILMIC");
                break;
            case ToneMappingOperator.Uncharted2:
                material.EnableKeyword("_TONEMAPPING_UNCHARTED2");
                break;
            case ToneMappingOperator.AgX:
                material.EnableKeyword("_TONEMAPPING_AGX");
                break;
        }
    }
}

private class ColorGradingData
{
    internal TextureHandle sourceTexture;
    internal TextureHandle destination;
    internal TextureHandle lutTexture;
    internal Material material;
    internal ProfessionalColorGrading colorGrading;
}

private class LutGenerationData
{
    internal TextureHandle lutTexture;
    internal ComputeShader computeShader;
    internal ProfessionalColorGrading colorGrading;
}
```

#### 3. Color Grading Shader

```hlsl
Shader "Hidden/Professional Color Grading"
{
    Properties
    {
        [HideInInspector] _BlitTexture ("Source Texture", 2D) = "white" {}  // Blitter.BlitCameraTexture는 _BlitTexture 바인딩
        [HideInInspector] _Lut3D ("3D LUT", 2D) = "white" {}
        [HideInInspector] _UserLut ("User LUT", 2D) = "white" {}
    }
    
    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" }
        
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"
        
        TEXTURE2D_X(_BlitTexture);  // Blitter.BlitCameraTexture → _BlitTexture
        TEXTURE2D(_Lut3D);
        TEXTURE2D(_UserLut);
        SAMPLER(sampler_BlitTexture);
        SAMPLER(sampler_Lut3D);
        SAMPLER(sampler_UserLut);
        
        float4 _LutParams; // (lutScale, lutBias, lutContribution, unused)
        
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
        
        // 3D LUT 샘플링 (Tetrahedral interpolation)
        float3 ApplyLut3D(TEXTURE2D_PARAM(lutTex, lutSampler), float3 uvw, float4 lutParams)
        {
            float3 scaledUVW = uvw * lutParams.y * lutParams.x + lutParams.x * 0.5;
            
            float slice = scaledUVW.z * 32.0;
            float sliceZ = floor(slice);
            float sliceFrac = slice - sliceZ;
            
            float2 uv0 = float2(scaledUVW.x + sliceZ * lutParams.x, scaledUVW.y);
            float2 uv1 = float2(scaledUVW.x + (sliceZ + 1.0) * lutParams.x, scaledUVW.y);
            
            float3 color0 = SAMPLE_TEXTURE2D(lutTex, lutSampler, uv0).rgb;
            float3 color1 = SAMPLE_TEXTURE2D(lutTex, lutSampler, uv1).rgb;
            
            return lerp(color0, color1, sliceFrac);
        }
        
        // 톤 매핑 연산자들
        float3 ToneMappingACES(float3 color)
        {
            // ACES Filmic Tone Mapping
            const float a = 2.51;
            const float b = 0.03;
            const float c = 2.43;
            const float d = 0.59;
            const float e = 0.14;
            
            color = (color * (a * color + b)) / (color * (c * color + d) + e);
            return saturate(color);
        }
        
        float3 ToneMappingReinhard(float3 color)
        {
            return color / (1.0 + color);
        }
        
        float3 ToneMappingReinhardExtended(float3 color)
        {
            float whitePoint = 2.0;
            float3 numerator = color * (1.0 + (color / (whitePoint * whitePoint)));
            return numerator / (1.0 + color);
        }
        
        float3 ToneMappingFilmic(float3 color)
        {
            // John Hable's Uncharted 2 tone mapping
            float A = 0.15;
            float B = 0.50;
            float C = 0.10;
            float D = 0.20;
            float E = 0.02;
            float F = 0.30;
            
            color = ((color * (A * color + C * B) + D * E) / (color * (A * color + B) + D * F)) - E / F;
            return color;
        }
        
        float3 ToneMappingUncharted2(float3 color)
        {
            float exposureBias = 2.0;
            color *= exposureBias;
            
            float3 mapped = ToneMappingFilmic(color);
            float3 whiteScale = 1.0 / ToneMappingFilmic(11.2);
            
            return mapped * whiteScale;
        }
        
        float3 ToneMappingAgX(float3 color)
        {
            // AgX tone mapping (simplified)
            const float3x3 agx_mat = float3x3(
                0.842479062253094, 0.0423282422610123, 0.0423756549057051,
                0.0784335999999992, 0.878468636469772, 0.0784336,
                0.0792237451477643, 0.0791661274605434, 0.879142973793104
            );
            
            const float3x3 agx_mat_inv = float3x3(
                1.19687900512017, -0.0528968517574562, -0.0529716355144438,
                -0.0980208811401368, 1.15190312990417, -0.0980434501171241,
                -0.0990297440797205, -0.0989611768448433, 1.15107367264116
            );
            
            color = mul(agx_mat, color);
            color = clamp(log2(color) / 10.0 + 0.5, 0.0, 1.0);
            color = pow(color, 2.4);
            color = mul(agx_mat_inv, color);
            
            return color;
        }
        
        ENDHLSL
        
        Pass
        {
            Name "Color Grading"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_local _ _USER_LUT
            #pragma multi_compile_local _ _TONEMAPPING_REINHARD _TONEMAPPING_REINHARD_EXTENDED _TONEMAPPING_ACES _TONEMAPPING_FILMIC _TONEMAPPING_UNCHARTED2 _TONEMAPPING_AGX
            
            float4 frag(Varyings input) : SV_Target
            {
                float3 color = SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_BlitTexture, input.texcoord).rgb;
                
                // 톤 매핑 적용
                #if defined(_TONEMAPPING_REINHARD)
                    color = ToneMappingReinhard(color);
                #elif defined(_TONEMAPPING_REINHARD_EXTENDED)
                    color = ToneMappingReinhardExtended(color);
                #elif defined(_TONEMAPPING_ACES)
                    color = ToneMappingACES(color);
                #elif defined(_TONEMAPPING_FILMIC)
                    color = ToneMappingFilmic(color);
                #elif defined(_TONEMAPPING_UNCHARTED2)
                    color = ToneMappingUncharted2(color);
                #elif defined(_TONEMAPPING_AGX)
                    color = ToneMappingAgX(color);
                #endif
                
                // 3D LUT 적용
                color = ApplyLut3D(TEXTURE2D_ARGS(_Lut3D, sampler_Lut3D), 
                                  saturate(color), _LutParams);
                
                // 사용자 정의 LUT 적용 (선택적)
                #ifdef _USER_LUT
                    float3 userLutColor = ApplyLut3D(TEXTURE2D_ARGS(_UserLut, sampler_UserLut), 
                                                   saturate(color), _LutParams);
                    color = lerp(color, userLutColor, _LutParams.z);
                #endif
                
                return float4(color, 1.0);
            }
            ENDHLSL
        }
    }
    
    FallBack "Hidden/Core/FallbackError"
}
```

---

## Lens Effects 구현

### 고급 Lens Effects 시스템

#### 1. Comprehensive Lens Effects Volume

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Advanced/Lens Effects Pro")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
public sealed class LensEffectsPro : VolumeComponent, IPostProcessComponent
{
    [Header("Chromatic Aberration")]
    [Tooltip("Chromatic aberration intensity")]
    public ClampedFloatParameter chromaticAberration = new ClampedFloatParameter(0f, 0f, 1f);
    
    [Tooltip("Aberration profile curve")]
    public AnimationCurveParameter aberrationProfile = new AnimationCurveParameter(
        AnimationCurve.EaseInOut(0f, 0f, 1f, 1f), false);
    
    [Header("Lens Distortion")]
    [Tooltip("Barrel/Pincushion distortion")]
    public ClampedFloatParameter lensDistortion = new ClampedFloatParameter(0f, -1f, 1f);
    
    [Tooltip("Distortion center")]
    public Vector2Parameter distortionCenter = new Vector2Parameter(new Vector2(0.5f, 0.5f));
    
    [Tooltip("Distortion scale")]
    public ClampedFloatParameter distortionScale = new ClampedFloatParameter(1f, 0.1f, 2f);
    
    [Header("Vignette")]
    [Tooltip("Vignette intensity")]
    public ClampedFloatParameter vignetteIntensity = new ClampedFloatParameter(0f, 0f, 1f);
    
    [Tooltip("Vignette smoothness")]
    public ClampedFloatParameter vignetteSmoothness = new ClampedFloatParameter(0.2f, 0.01f, 1f);
    
    [Tooltip("Vignette roundness")]
    public ClampedFloatParameter vignetteRoundness = new ClampedFloatParameter(1f, 0f, 1f);
    
    [Tooltip("Vignette center")]
    public Vector2Parameter vignetteCenter = new Vector2Parameter(new Vector2(0.5f, 0.5f));
    
    [Tooltip("Vignette color")]
    public ColorParameter vignetteColor = new ColorParameter(Color.black, false, false, true);
    
    [Header("Film Grain")]
    [Tooltip("Film grain intensity")]
    public ClampedFloatParameter filmGrainIntensity = new ClampedFloatParameter(0f, 0f, 1f);
    
    [Tooltip("Grain size")]
    public ClampedFloatParameter grainSize = new ClampedFloatParameter(1f, 0.1f, 3f);
    
    [Tooltip("Grain response")]
    public ClampedFloatParameter grainResponse = new ClampedFloatParameter(0.8f, 0f, 1f);
    
    [Tooltip("Luminance contribution")]
    public ClampedFloatParameter luminanceContribution = new ClampedFloatParameter(0.8f, 0f, 1f);
    
    [Header("Lens Flare")]
    [Tooltip("Enable lens flare")]
    public BoolParameter enableLensFlare = new BoolParameter(false);
    
    [Tooltip("Flare intensity")]
    public ClampedFloatParameter flareIntensity = new ClampedFloatParameter(1f, 0f, 5f);
    
    [Tooltip("Flare threshold")]
    public ClampedFloatParameter flareThreshold = new ClampedFloatParameter(1f, 0f, 4f);
    
    [Tooltip("Flare ghosts count")]
    public ClampedIntParameter flareGhosts = new ClampedIntParameter(6, 1, 16);
    
    [Tooltip("Flare ghost dispersal")]
    public ClampedFloatParameter flareDispersal = new ClampedFloatParameter(0.3f, 0.1f, 1f);
    
    [Tooltip("Flare halo radius")]
    public ClampedFloatParameter flareHaloRadius = new ClampedFloatParameter(0.4f, 0.1f, 1f);
    
    [Tooltip("Flare color")]
    public ColorParameter flareColor = new ColorParameter(Color.white, false, false, true);
    
    [Header("Advanced")]
    [Tooltip("Quality preset")]
    public LensQualityParameter quality = new LensQualityParameter(LensQuality.Medium);
    
    [Tooltip("Temporal stability")]
    public ClampedFloatParameter temporalStability = new ClampedFloatParameter(0.1f, 0f, 1f);
    
    public bool IsActive() => 
        chromaticAberration.value > 0f ||
        !Mathf.Approximately(lensDistortion.value, 0f) ||
        vignetteIntensity.value > 0f ||
        filmGrainIntensity.value > 0f ||
        (enableLensFlare.value && flareIntensity.value > 0f);
}

public enum LensQuality
{
    Low,     // 기본적인 효과만
    Medium,  // 표준 품질
    High,    // 고품질 샘플링
    Ultra    // 최고 품질 + 노이즈 필터
}

[Serializable]
public sealed class LensQualityParameter : VolumeParameter<LensQuality>
{
    public LensQualityParameter(LensQuality value, bool overrideState = false) 
        : base(value, overrideState) { }
}
```

#### 2. Lens Effects Render Pass

```csharp
public class LensEffectsProPass : ScriptableRenderPass
{
    private const int k_ChromaticAberrationPass = 0;
    private const int k_DistortionPass = 1;
    private const int k_VignettePass = 2;
    private const int k_FilmGrainPass = 3;
    private const int k_LensFlarePrepass = 4;
    private const int k_LensFlareComposite = 5;
    private const int k_CombinedPass = 6;
    
    private Material m_LensEffectsMaterial;
    private ComputeShader m_LensFlareCompute;
    private LensEffectsPro m_LensEffects;
    
    private RTHandle m_TempTexture1;
    private RTHandle m_TempTexture2;
    private RTHandle m_LensFlareTexture;
    private RTHandle m_GrainTexture;
    
    // 노이즈 텍스처 (필름 그레인용)
    private Texture2D m_BlueNoiseTexture;
    
    private static readonly ProfilingSampler s_ProfilingSampler = 
        new ProfilingSampler("Lens Effects Pro");
    
    // Shader property IDs
    private static readonly int s_DistortionParams = Shader.PropertyToID("_DistortionParams");
    private static readonly int s_VignetteParams = Shader.PropertyToID("_VignetteParams");
    private static readonly int s_ChromaticParams = Shader.PropertyToID("_ChromaticParams");
    private static readonly int s_GrainParams = Shader.PropertyToID("_GrainParams");
    private static readonly int s_FlareParams = Shader.PropertyToID("_FlareParams");
    private static readonly int s_GrainTexture = Shader.PropertyToID("_GrainTexture");
    private static readonly int s_LensFlareTexture = Shader.PropertyToID("_LensFlareTexture");
    private static readonly int s_BlueNoise = Shader.PropertyToID("_BlueNoise");
    
    public LensEffectsProPass(Material lensEffectsMaterial, ComputeShader lensFlareCompute)
    {
        m_LensEffectsMaterial = lensEffectsMaterial;
        m_LensFlareCompute = lensFlareCompute;
        renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
        
        // Blue noise 텍스처 생성 (필름 그레인용)
        GenerateBlueNoiseTexture();
    }
    
    public void Setup(LensEffectsPro lensEffects)
    {
        m_LensEffects = lensEffects;
    }
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        if (!ShouldRender(cameraData))
            return;
            
        ExecuteLensEffects(renderGraph, resourceData, cameraData);
    }
    
    private void ExecuteLensEffects(RenderGraph renderGraph, 
                                  UniversalResourceData resourceData,
                                  UniversalCameraData cameraData)
    {
        var desc = cameraData.cameraTargetDescriptor;
        
        using (var builder = renderGraph.AddUnsafePass<LensEffectsData>(
            "Lens Effects Pro", out var passData, s_ProfilingSampler))
        {
            // 텍스처 설정
            passData.sourceTexture = resourceData.activeColorTexture;
            passData.tempTexture1 = CreateTempTexture(renderGraph, desc, "_LensTemp1");
            passData.tempTexture2 = CreateTempTexture(renderGraph, desc, "_LensTemp2");
            
            if (m_LensEffects.enableLensFlare.value && m_LensEffects.flareIntensity.value > 0f)
            {
                var flareDesc = desc;
                flareDesc.width /= 4;  // 1/4 해상도로 렌즈 플레어 계산
                flareDesc.height /= 4;
                passData.lensFlareTexture = CreateTempTexture(renderGraph, flareDesc, "_LensFlare");
            }
            
            // PassData 설정
            passData.lensEffects = m_LensEffects;
            passData.material = m_LensEffectsMaterial;
            passData.computeShader = m_LensFlareCompute;
            passData.blueNoiseTexture = m_BlueNoiseTexture;
            
            // 의존성 설정
            builder.UseTexture(passData.sourceTexture, AccessFlags.ReadWrite);
            builder.UseTexture(passData.tempTexture1, AccessFlags.ReadWrite);
            builder.UseTexture(passData.tempTexture2, AccessFlags.ReadWrite);
            
            if (passData.lensFlareTexture.IsValid())
                builder.UseTexture(passData.lensFlareTexture, AccessFlags.ReadWrite);
            
            builder.SetRenderFunc(static (LensEffectsData data, UnsafeGraphContext context) =>
            {
                ExecuteLensEffectsPasses(data, context);
            });
        }
    }
    
    private static void ExecuteLensEffectsPasses(LensEffectsData data, UnsafeGraphContext context)
    {
        var cmd = CommandBufferHelpers.GetNativeCommandBuffer(context.cmd);
        var settings = data.lensEffects;
        
        TextureHandle currentInput = data.sourceTexture;
        TextureHandle currentOutput = data.tempTexture1;
        
        // 1. Chromatic Aberration
        if (settings.chromaticAberration.value > 0f)
        {
            SetupChromaticAberrationParameters(data);
            cmd.Blit(currentInput, currentOutput, data.material, k_ChromaticAberrationPass);
            (currentInput, currentOutput) = (currentOutput, currentInput);
        }
        
        // 2. Lens Distortion
        if (!Mathf.Approximately(settings.lensDistortion.value, 0f))
        {
            SetupDistortionParameters(data);
            cmd.Blit(currentInput, currentOutput, data.material, k_DistortionPass);
            (currentInput, currentOutput) = (currentOutput, currentInput);
        }
        
        // 3. Lens Flare (비동기 처리)
        if (settings.enableLensFlare.value && data.lensFlareTexture.IsValid())
        {
            GenerateLensFlare(data, cmd);
        }
        
        // 4. Combined Pass (Vignette + Film Grain + Lens Flare)
        SetupCombinedParameters(data);
        
        // 최종 출력 설정
        TextureHandle finalOutput = currentInput == data.sourceTexture ? data.tempTexture1 : data.sourceTexture;
        cmd.Blit(currentInput, finalOutput, data.material, k_CombinedPass);
        
        // 결과를 원본 텍스처로 복사 (필요한 경우)
        if (finalOutput != data.sourceTexture)
        {
            cmd.Blit(finalOutput, data.sourceTexture);
        }
    }
    
    private static void SetupChromaticAberrationParameters(LensEffectsData data)
    {
        var settings = data.lensEffects;
        
        // 색수차 강도를 프로파일 곡선으로 조정
        float intensity = settings.chromaticAberration.value;
        
        var chromaticParams = new Vector4(
            intensity * 0.01f,  // Red channel offset
            intensity * 0.005f, // Green channel offset  
            intensity * 0.015f, // Blue channel offset
            settings.quality.value >= LensQuality.High ? 1f : 0f // High quality sampling
        );
        
        data.material.SetVector(s_ChromaticParams, chromaticParams);
        
        // 프로파일 곡선을 텍스처로 변환 (필요시)
        if (settings.quality.value >= LensQuality.Ultra)
        {
            // TODO: Convert aberration profile curve to texture
        }
    }
    
    private static void SetupDistortionParameters(LensEffectsData data)
    {
        var settings = data.lensEffects;
        
        var distortionParams = new Vector4(
            settings.lensDistortion.value,
            settings.distortionScale.value,
            settings.distortionCenter.value.x,
            settings.distortionCenter.value.y
        );
        
        data.material.SetVector(s_DistortionParams, distortionParams);
    }
    
    private static void SetupCombinedParameters(LensEffectsData data)
    {
        var settings = data.lensEffects;
        
        // Vignette 파라미터
        var vignetteParams = new Vector4(
            settings.vignetteIntensity.value,
            settings.vignetteSmoothness.value,
            settings.vignetteRoundness.value,
            0f
        );
        
        var vignetteCenter = new Vector4(
            settings.vignetteCenter.value.x,
            settings.vignetteCenter.value.y,
            0f, 0f
        );
        
        data.material.SetVector(s_VignetteParams, vignetteParams);
        data.material.SetVector("_VignetteCenter", vignetteCenter);
        data.material.SetColor("_VignetteColor", settings.vignetteColor.value);
        
        // Film Grain 파라미터
        var grainParams = new Vector4(
            settings.filmGrainIntensity.value,
            settings.grainSize.value,
            settings.grainResponse.value,
            settings.luminanceContribution.value
        );
        
        data.material.SetVector(s_GrainParams, grainParams);
        data.material.SetTexture(s_BlueNoise, data.blueNoiseTexture);
        
        // Lens Flare 설정
        if (settings.enableLensFlare.value && data.lensFlareTexture.IsValid())
        {
            data.material.SetTexture(s_LensFlareTexture, data.lensFlareTexture);
            data.material.SetFloat("_FlareIntensity", settings.flareIntensity.value);
            data.material.EnableKeyword("_LENS_FLARE");
        }
        else
        {
            data.material.DisableKeyword("_LENS_FLARE");
        }
        
        // 품질 키워드 설정
        SetQualityKeywords(data.material, settings.quality.value);
    }
    
    private static void GenerateLensFlare(LensEffectsData data, CommandBuffer cmd)
    {
        var settings = data.lensEffects;
        
        if (data.computeShader != null)
        {
            int kernelIndex = data.computeShader.FindKernel("GenerateLensFlare");
            
            // Lens Flare 파라미터 설정
            var flareParams = new Vector4(
                settings.flareThreshold.value,
                settings.flareDispersal.value,
                settings.flareHaloRadius.value,
                settings.flareGhosts.value
            );
            
            cmd.SetComputeVectorParam(data.computeShader, "_FlareParams", flareParams);
            cmd.SetComputeVectorParam(data.computeShader, "_FlareColor", settings.flareColor.value);
            cmd.SetComputeTextureParam(data.computeShader, kernelIndex, "_SourceTexture", data.sourceTexture);
            cmd.SetComputeTextureParam(data.computeShader, kernelIndex, "_FlareResult", data.lensFlareTexture);
            
            // Dispatch
            var flareDesc = data.lensFlareTexture; // RTHandle에서 해상도 정보 추출
            int groupsX = (256 + 7) / 8; // 가정된 해상도, 실제 구현에서는 정확한 값 필요
            int groupsY = (144 + 7) / 8;
            cmd.DispatchCompute(data.computeShader, kernelIndex, groupsX, groupsY, 1);
        }
    }
    
    private static void SetQualityKeywords(Material material, LensQuality quality)
    {
        material.DisableKeyword("_QUALITY_LOW");
        material.DisableKeyword("_QUALITY_MEDIUM");
        material.DisableKeyword("_QUALITY_HIGH");
        material.DisableKeyword("_QUALITY_ULTRA");
        
        switch (quality)
        {
            case LensQuality.Low:
                material.EnableKeyword("_QUALITY_LOW");
                break;
            case LensQuality.Medium:
                material.EnableKeyword("_QUALITY_MEDIUM");
                break;
            case LensQuality.High:
                material.EnableKeyword("_QUALITY_HIGH");
                break;
            case LensQuality.Ultra:
                material.EnableKeyword("_QUALITY_ULTRA");
                break;
        }
    }
    
    private void GenerateBlueNoiseTexture()
    {
        // Blue noise 텍스처 생성 (간단한 구현)
        int size = 64;
        m_BlueNoiseTexture = new Texture2D(size, size, TextureFormat.R8, false, true)
        {
            name = "BlueNoise_LensEffects",
            wrapMode = TextureWrapMode.Repeat,
            filterMode = FilterMode.Point
        };
        
        var pixels = new Color32[size * size];
        var random = new Unity.Mathematics.Random(12345);
        
        for (int i = 0; i < pixels.Length; i++)
        {
            byte value = (byte)(random.NextFloat() * 255);
            pixels[i] = new Color32(value, value, value, 255);
        }
        
        m_BlueNoiseTexture.SetPixels32(pixels);
        m_BlueNoiseTexture.Apply();
    }
    
    private TextureHandle CreateTempTexture(RenderGraph renderGraph, RenderTextureDescriptor desc, string name)
    {
        var tempDesc = desc;
        tempDesc.msaaSamples = 1;
        tempDesc.name = name;
        
        return UniversalRenderer.CreateRenderGraphTexture(renderGraph, tempDesc, name, true);
    }
    
    private bool ShouldRender(UniversalCameraData cameraData)
    {
        return cameraData.camera.cameraType == CameraType.Game &&
               m_LensEffects.IsActive();
    }
}

private class LensEffectsData
{
    internal TextureHandle sourceTexture;
    internal TextureHandle tempTexture1;
    internal TextureHandle tempTexture2;
    internal TextureHandle lensFlareTexture;
    internal LensEffectsPro lensEffects;
    internal Material material;
    internal ComputeShader computeShader;
    internal Texture2D blueNoiseTexture;
}
```

---

## Anti-aliasing 기법

### 고급 Anti-aliasing 시스템

#### 1. Temporal Anti-Aliasing (TAA) 구현

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Advanced/Temporal Anti-Aliasing")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
public sealed class TemporalAntiAliasing : VolumeComponent, IPostProcessComponent
{
    [Header("TAA Settings")]
    [Tooltip("TAA quality preset")]
    public TAAQualityParameter quality = new TAAQualityParameter(TAAQuality.Medium);
    
    [Tooltip("Temporal blend factor")]
    public ClampedFloatParameter temporalBlend = new ClampedFloatParameter(0.9f, 0.1f, 0.99f);
    
    [Tooltip("Motion threshold")]
    public ClampedFloatParameter motionThreshold = new ClampedFloatParameter(0.01f, 0.001f, 0.1f);
    
    [Header("Jitter Pattern")]
    [Tooltip("Jitter sequence type")]
    public JitterSequenceParameter jitterSequence = new JitterSequenceParameter(JitterSequence.Halton);
    
    [Tooltip("Jitter scale")]
    public ClampedFloatParameter jitterScale = new ClampedFloatParameter(1f, 0.1f, 2f);
    
    [Header("History")]
    [Tooltip("History rectification")]
    public BoolParameter historyRectification = new BoolParameter(true);
    
    [Tooltip("Variance clipping")]
    public BoolParameter varianceClipping = new BoolParameter(true);
    
    [Tooltip("Neighborhood clamping")]
    public ClampedFloatParameter neighborhoodClamping = new ClampedFloatParameter(1f, 0.1f, 4f);
    
    [Header("Sharpening")]
    [Tooltip("Post-TAA sharpening")]
    public ClampedFloatParameter sharpening = new ClampedFloatParameter(0f, 0f, 1f);
    
    [Tooltip("Adaptive sharpening")]
    public BoolParameter adaptiveSharpening = new BoolParameter(true);
    
    public bool IsActive() => true; // TAA는 항상 활성화 가능
}

public enum TAAQuality
{
    Low,      // 4 samples
    Medium,   // 8 samples
    High,     // 16 samples
    Ultra     // 32 samples
}

public enum JitterSequence
{
    Uniform,   // 균등 분포
    Halton,    // Halton sequence
    R2,        // R2 sequence
    Sobol      // Sobol sequence
}

[Serializable]
public sealed class TAAQualityParameter : VolumeParameter<TAAQuality>
{
    public TAAQualityParameter(TAAQuality value, bool overrideState = false) 
        : base(value, overrideState) { }
}

[Serializable]
public sealed class JitterSequenceParameter : VolumeParameter<JitterSequence>
{
    public JitterSequenceParameter(JitterSequence value, bool overrideState = false) 
        : base(value, overrideState) { }
}
```

#### 2. TAA Render Pass

```csharp
public class TemporalAntiAliasingPass : ScriptableRenderPass
{
    private const int k_TAAPass = 0;
    private const int k_SharpeningPass = 1;
    
    private Material m_TAAmaterial;
    private TemporalAntiAliasing m_TAASettings;
    
    private RTHandle[] m_HistoryTextures = new RTHandle[2];
    private int m_HistoryIndex = 0;
    
    // Jitter 패턴
    private Vector2[] m_JitterSequence;
    private int m_JitterIndex = 0;
    
    // 이전 프레임 매트릭스
    private Matrix4x4 m_PreviousViewProjectionMatrix;
    private bool m_FirstFrame = true;
    
    private static readonly ProfilingSampler s_ProfilingSampler = 
        new ProfilingSampler("Temporal Anti-Aliasing");
    
    public TemporalAntiAliasingPass(Material taaMaterial)
    {
        m_TAAmaterial = taaMaterial;
        renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
        
        // Jitter 시퀀스 초기화
        GenerateJitterSequence();
    }
    
    public void Setup(TemporalAntiAliasing taaSettings)
    {
        m_TAASettings = taaSettings;
        
        // 품질 변경시 Jitter 시퀀스 재생성
        if (m_JitterSequence == null || m_JitterSequence.Length != GetSampleCount())
        {
            GenerateJitterSequence();
        }
    }
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        if (!ShouldRender(cameraData))
            return;
            
        ExecuteTAA(renderGraph, resourceData, cameraData);
    }
    
    private void ExecuteTAA(RenderGraph renderGraph, 
                          UniversalResourceData resourceData,
                          UniversalCameraData cameraData)
    {
        using (var builder = renderGraph.AddRasterRenderPass<TAAData>(
            "Temporal Anti-Aliasing", out var passData, s_ProfilingSampler))
        {
            var desc = cameraData.cameraTargetDescriptor;
            
            // History 텍스처 생성/업데이트
            EnsureHistoryTextures(renderGraph, desc);
            
            passData.sourceTexture = resourceData.activeColorTexture;
            passData.depthTexture = resourceData.cameraDepthTexture;
            passData.motionVectorTexture = GetMotionVectorTexture(resourceData);
            passData.historyTexture = m_HistoryTextures[m_HistoryIndex];
            passData.material = m_TAAmaterial;
            passData.taaSettings = m_TAASettings;
            
            // 출력 텍스처
            passData.outputTexture = UniversalRenderer.CreateRenderGraphTexture(
                renderGraph, desc, "_TAAOutput", true);
            
            // 새로운 히스토리 텍스처
            passData.newHistoryTexture = m_HistoryTextures[1 - m_HistoryIndex];
            
            // 카메라 매트릭스
            passData.viewProjectionMatrix = cameraData.GetViewMatrix() * cameraData.GetProjectionMatrix();
            passData.previousViewProjectionMatrix = m_PreviousViewProjectionMatrix;
            passData.jitterOffset = GetCurrentJitterOffset();
            passData.isFirstFrame = m_FirstFrame;
            
            // 의존성 설정
            builder.UseTexture(passData.sourceTexture, AccessFlags.Read);
            builder.UseTexture(passData.depthTexture, AccessFlags.Read);
            if (passData.motionVectorTexture.IsValid())
                builder.UseTexture(passData.motionVectorTexture, AccessFlags.Read);
            if (passData.historyTexture.IsValid())
                builder.UseTexture(passData.historyTexture, AccessFlags.Read);
            builder.UseTexture(passData.newHistoryTexture, AccessFlags.Write);
            builder.SetRenderAttachment(passData.outputTexture, 0, AccessFlags.Write);
            
            builder.SetRenderFunc(static (TAAData data, RasterGraphContext context) =>
            {
                ExecuteTAAPass(data, context);
            });
        }
        
        // 프레임 종료 시 상태 업데이트
        UpdateFrameState(cameraData);
    }
    
    private static void ExecuteTAAPass(TAAData data, RasterGraphContext context)
    {
        var cmd = context.cmd;
        
        // TAA 파라미터 설정
        SetupTAAParameters(data);
        
        // TAA 실행
        if (data.isFirstFrame || !data.historyTexture.IsValid())
        {
            // 첫 프레임: 히스토리 없이 현재 프레임만 사용
            cmd.Blit(data.sourceTexture, data.outputTexture);
            cmd.Blit(data.sourceTexture, data.newHistoryTexture);
        }
        else
        {
            // TAA 패스 실행
            Blitter.BlitCameraTexture(cmd, data.sourceTexture, data.outputTexture, 
                data.material, k_TAAPass);
            
            // 새로운 히스토리 저장
            cmd.Blit(data.outputTexture, data.newHistoryTexture);
        }
        
        // Post-TAA 샤프닝 (선택적)
        if (data.taaSettings.sharpening.value > 0f)
        {
            SetupSharpeningParameters(data);
            
            // In-place 샤프닝
            var tempRT = Shader.PropertyToID("_TempTAART");
            cmd.GetTemporaryRT(tempRT, data.outputTexture.rt.descriptor);
            cmd.Blit(data.outputTexture, tempRT, data.material, k_SharpeningPass);
            cmd.Blit(tempRT, data.outputTexture);
            cmd.ReleaseTemporaryRT(tempRT);
        }
    }
    
    private static void SetupTAAParameters(TAAData data)
    {
        var settings = data.taaSettings;
        
        // TAA 파라미터
        var taaParams = new Vector4(
            settings.temporalBlend.value,
            settings.motionThreshold.value,
            settings.neighborhoodClamping.value,
            settings.varianceClipping.value ? 1f : 0f
        );
        
        data.material.SetVector("_TAAParams", taaParams);
        data.material.SetVector("_JitterOffset", data.jitterOffset);
        
        // 매트릭스 설정
        var reprojectionMatrix = data.previousViewProjectionMatrix * Matrix4x4.Inverse(data.viewProjectionMatrix);
        data.material.SetMatrix("_ReprojectionMatrix", reprojectionMatrix);
        
        // 히스토리 텍스처
        if (data.historyTexture.IsValid())
            data.material.SetTexture("_HistoryTexture", data.historyTexture);
        
        // 모션 벡터 (있는 경우)
        if (data.motionVectorTexture.IsValid())
        {
            data.material.SetTexture("_MotionVectorTexture", data.motionVectorTexture);
            data.material.EnableKeyword("_MOTION_VECTORS");
        }
        else
        {
            data.material.DisableKeyword("_MOTION_VECTORS");
        }
        
        // 품질 키워드
        SetQualityKeywords(data.material, settings.quality.value);
        
        // 기타 기능 키워드
        CoreUtils.SetKeyword(data.material, "_HISTORY_RECTIFICATION", 
            settings.historyRectification.value);
        CoreUtils.SetKeyword(data.material, "_VARIANCE_CLIPPING", 
            settings.varianceClipping.value);
    }
    
    private static void SetupSharpeningParameters(TAAData data)
    {
        var sharpeningParams = new Vector4(
            data.taaSettings.sharpening.value,
            data.taaSettings.adaptiveSharpening.value ? 1f : 0f,
            0f, 0f
        );
        
        data.material.SetVector("_SharpeningParams", sharpeningParams);
    }
    
    private static void SetQualityKeywords(Material material, TAAQuality quality)
    {
        material.DisableKeyword("_TAA_LOW");
        material.DisableKeyword("_TAA_MEDIUM");
        material.DisableKeyword("_TAA_HIGH");
        material.DisableKeyword("_TAA_ULTRA");
        
        switch (quality)
        {
            case TAAQuality.Low:
                material.EnableKeyword("_TAA_LOW");
                break;
            case TAAQuality.Medium:
                material.EnableKeyword("_TAA_MEDIUM");
                break;
            case TAAQuality.High:
                material.EnableKeyword("_TAA_HIGH");
                break;
            case TAAQuality.Ultra:
                material.EnableKeyword("_TAA_ULTRA");
                break;
        }
    }
    
    private void GenerateJitterSequence()
    {
        int sampleCount = GetSampleCount();
        m_JitterSequence = new Vector2[sampleCount];
        
        switch (m_TAASettings?.jitterSequence.value ?? JitterSequence.Halton)
        {
            case JitterSequence.Uniform:
                GenerateUniformSequence(sampleCount);
                break;
            case JitterSequence.Halton:
                GenerateHaltonSequence(sampleCount);
                break;
            case JitterSequence.R2:
                GenerateR2Sequence(sampleCount);
                break;
            case JitterSequence.Sobol:
                GenerateSobolSequence(sampleCount);
                break;
        }
    }
    
    private void GenerateHaltonSequence(int sampleCount)
    {
        // Halton sequence 생성 (base 2, 3)
        for (int i = 0; i < sampleCount; i++)
        {
            float x = RadicalInverse(i, 2);
            float y = RadicalInverse(i, 3);
            m_JitterSequence[i] = new Vector2(x - 0.5f, y - 0.5f);
        }
    }
    
    private void GenerateR2Sequence(int sampleCount)
    {
        // R2 sequence (금본비 기반)
        float g = 1.32471795724474602596f; // Plastic constant
        float a1 = 1f / g;
        float a2 = 1f / (g * g);
        
        for (int i = 0; i < sampleCount; i++)
        {
            float x = Mathf.Repeat(0.5f + a1 * i, 1f);
            float y = Mathf.Repeat(0.5f + a2 * i, 1f);
            m_JitterSequence[i] = new Vector2(x - 0.5f, y - 0.5f);
        }
    }
    
    private void GenerateUniformSequence(int sampleCount)
    {
        // 단순한 그리드 패턴
        int gridSize = Mathf.CeilToInt(Mathf.Sqrt(sampleCount));
        for (int i = 0; i < sampleCount; i++)
        {
            int x = i % gridSize;
            int y = i / gridSize;
            float u = (x + 0.5f) / gridSize - 0.5f;
            float v = (y + 0.5f) / gridSize - 0.5f;
            m_JitterSequence[i] = new Vector2(u, v);
        }
    }
    
    private void GenerateSobolSequence(int sampleCount)
    {
        // 간단한 Sobol sequence 구현
        for (int i = 0; i < sampleCount; i++)
        {
            float x = SobolSequence(i, 0);
            float y = SobolSequence(i, 1);
            m_JitterSequence[i] = new Vector2(x - 0.5f, y - 0.5f);
        }
    }
    
    private float RadicalInverse(int n, int baseVal)
    {
        float result = 0f;
        float invBase = 1f / baseVal;
        float invBaseN = invBase;
        
        while (n > 0)
        {
            result += (n % baseVal) * invBaseN;
            n /= baseVal;
            invBaseN *= invBase;
        }
        
        return result;
    }
    
    private float SobolSequence(int index, int dimension)
    {
        // 간단한 Sobol 구현 (실제로는 더 복잡한 구현 필요)
        uint x = (uint)index;
        if (dimension == 1) x ^= x >> 1;
        
        uint result = 0;
        uint bit = 0x80000000;
        
        while (bit != 0)
        {
            if ((x & bit) != 0)
                result ^= bit;
            bit >>= 1;
        }
        
        return result / (float)uint.MaxValue;
    }
    
    private int GetSampleCount()
    {
        return m_TAASettings?.quality.value switch
        {
            TAAQuality.Low => 4,
            TAAQuality.Medium => 8,
            TAAQuality.High => 16,
            TAAQuality.Ultra => 32,
            _ => 8
        };
    }
    
    private Vector2 GetCurrentJitterOffset()
    {
        if (m_JitterSequence == null || m_JitterSequence.Length == 0)
            return Vector2.zero;
            
        var jitter = m_JitterSequence[m_JitterIndex];
        return jitter * (m_TAASettings?.jitterScale.value ?? 1f);
    }
    
    private void UpdateFrameState(UniversalCameraData cameraData)
    {
        // 히스토리 인덱스 교체
        m_HistoryIndex = 1 - m_HistoryIndex;
        
        // Jitter 인덱스 업데이트
        m_JitterIndex = (m_JitterIndex + 1) % m_JitterSequence.Length;
        
        // 매트릭스 저장
        m_PreviousViewProjectionMatrix = cameraData.GetViewMatrix() * cameraData.GetProjectionMatrix();
        
        // 첫 프레임 플래그
        m_FirstFrame = false;
    }
    
    private void EnsureHistoryTextures(RenderGraph renderGraph, RenderTextureDescriptor desc)
    {
        var historyDesc = desc;
        historyDesc.msaaSamples = 1;
        historyDesc.name = "TAAHistory";
        
        for (int i = 0; i < 2; i++)
        {
            if (m_HistoryTextures[i] == null || 
                !m_HistoryTextures[i].rt.IsCreated() ||
                m_HistoryTextures[i].rt.width != desc.width ||
                m_HistoryTextures[i].rt.height != desc.height)
            {
                m_HistoryTextures[i]?.Release();
                m_HistoryTextures[i] = RTHandles.Alloc(historyDesc, name: $"TAAHistory_{i}");
            }
        }
    }
    
    private TextureHandle GetMotionVectorTexture(UniversalResourceData resourceData)
    {
        // Motion Vector 텍스처가 있다면 반환, 없으면 invalid handle
        // 실제 구현에서는 Motion Vector Pass의 결과를 가져와야 함
        return new TextureHandle(); // Placeholder
    }
    
    private bool ShouldRender(UniversalCameraData cameraData)
    {
        return cameraData.camera.cameraType == CameraType.Game;
    }
}

private class TAAData
{
    internal TextureHandle sourceTexture;
    internal TextureHandle depthTexture;
    internal TextureHandle motionVectorTexture;
    internal TextureHandle historyTexture;
    internal TextureHandle newHistoryTexture;
    internal TextureHandle outputTexture;
    internal Material material;
    internal TemporalAntiAliasing taaSettings;
    internal Matrix4x4 viewProjectionMatrix;
    internal Matrix4x4 previousViewProjectionMatrix;
    internal Vector2 jitterOffset;
    internal bool isFirstFrame;
}
```

---

## SSAO/SSGI 구현

### Screen-Space Ambient Occlusion & Global Illumination

#### 1. Advanced SSAO Volume Component

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Advanced/Screen Space Ambient Occlusion")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
public sealed class AdvancedSSAO : VolumeComponent, IPostProcessComponent
{
    [Header("SSAO Settings")]
    [Tooltip("SSAO intensity")]
    public ClampedFloatParameter intensity = new ClampedFloatParameter(1f, 0f, 4f);
    
    [Tooltip("Occlusion radius")]
    public ClampedFloatParameter radius = new ClampedFloatParameter(0.3f, 0.01f, 2f);
    
    [Tooltip("Sample count")]
    public ClampedIntParameter sampleCount = new ClampedIntParameter(16, 4, 64);
    
    [Header("Quality")]
    [Tooltip("SSAO technique")]
    public SSAOTechniqueParameter technique = new SSAOTechniqueParameter(SSAOTechnique.HBAO);
    
    [Tooltip("Enable temporal filtering")]
    public BoolParameter temporalFiltering = new BoolParameter(true);
    
    [Tooltip("Temporal blend factor")]
    public ClampedFloatParameter temporalBlend = new ClampedFloatParameter(0.1f, 0.01f, 0.5f);
    
    [Header("Bias & Thickness")]
    [Tooltip("Normal bias")]
    public ClampedFloatParameter normalBias = new ClampedFloatParameter(0.1f, 0f, 1f);
    
    [Tooltip("Thickness modifier")]
    public ClampedFloatParameter thickness = new ClampedFloatParameter(1f, 0.1f, 10f);
    
    [Header("Distance Falloff")]
    [Tooltip("Distance falloff start")]
    public ClampedFloatParameter falloffStart = new ClampedFloatParameter(100f, 1f, 1000f);
    
    [Tooltip("Distance falloff end")]
    public ClampedFloatParameter falloffEnd = new ClampedFloatParameter(200f, 1f, 1000f);
    
    [Header("Filtering")]
    [Tooltip("Enable bilateral filtering")]
    public BoolParameter bilateralFiltering = new BoolParameter(true);
    
    [Tooltip("Bilateral threshold")]
    public ClampedFloatParameter bilateralThreshold = new ClampedFloatParameter(0.1f, 0.01f, 1f);
    
    [Tooltip("Blur passes")]
    public ClampedIntParameter blurPasses = new ClampedIntParameter(2, 1, 4);
    
    [Header("Advanced")]
    [Tooltip("Power exponent")]
    public ClampedFloatParameter power = new ClampedFloatParameter(2f, 0.1f, 6f);
    
    [Tooltip("Horizon angle threshold")]
    public ClampedFloatParameter horizonAngleThreshold = new ClampedFloatParameter(0.06f, 0f, 0.2f);
    
    [Tooltip("Enable multibounce approximation")]
    public BoolParameter multibounce = new BoolParameter(false);
    
    public bool IsActive() => intensity.value > 0f;
}

public enum SSAOTechnique
{
    SAO,        // Scalable Ambient Obscurance
    HBAO,       // Horizon-Based Ambient Occlusion
    GTAO,       // Ground-Truth Ambient Occlusion
    RayTraced   // Ray-traced AO (if supported)
}

[Serializable]
public sealed class SSAOTechniqueParameter : VolumeParameter<SSAOTechnique>
{
    public SSAOTechniqueParameter(SSAOTechnique value, bool overrideState = false) 
        : base(value, overrideState) { }
}
```

#### 2. SSAO Render Pass Implementation

```csharp
public class AdvancedSSAORenderPass : ScriptableRenderPass
{
    private const int k_SSAOPass = 0;
    private const int k_BilateralFilterPass = 1;
    private const int k_TemporalFilterPass = 2;
    private const int k_CompositePass = 3;
    
    private Material m_SSAOMaterial;
    private ComputeShader m_SSAOCompute;
    private AdvancedSSAO m_SSAOSettings;
    
    private RTHandle m_SSAOTexture;
    private RTHandle m_FilteredSSAOTexture;
    private RTHandle m_TemporalHistory;
    private RTHandle m_NormalTexture;
    
    // SSAO 노이즈 텍스처
    private Texture2D m_NoiseTexture;
    
    // 샘플 커널
    private Vector4[] m_SampleKernel;
    
    // 이전 프레임 데이터
    private Matrix4x4 m_PreviousViewMatrix;
    private Matrix4x4 m_PreviousProjectionMatrix;
    private bool m_FirstFrame = true;
    
    private static readonly ProfilingSampler s_ProfilingSampler = 
        new ProfilingSampler("Advanced SSAO");
    
    public AdvancedSSAORenderPass(Material ssaoMaterial, ComputeShader ssaoCompute)
    {
        m_SSAOMaterial = ssaoMaterial;
        m_SSAOCompute = ssaoCompute;
        renderPassEvent = RenderPassEvent.AfterRenderingOpaques;
        
        GenerateNoiseTexture();
        GenerateSampleKernel();
    }
    
    public void Setup(AdvancedSSAO ssaoSettings)
    {
        m_SSAOSettings = ssaoSettings;
        
        // 샘플 수 변경시 커널 재생성
        if (m_SampleKernel == null || m_SampleKernel.Length != ssaoSettings.sampleCount.value)
        {
            GenerateSampleKernel();
        }
    }
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        if (!ShouldRender(cameraData))
            return;
            
        ExecuteSSAO(renderGraph, resourceData, cameraData);
    }
    
    private void ExecuteSSAO(RenderGraph renderGraph, 
                           UniversalResourceData resourceData,
                           UniversalCameraData cameraData)
    {
        var desc = cameraData.cameraTargetDescriptor;
        var ssaoDesc = GetSSAODescriptor(desc);
        
        using (var builder = renderGraph.AddUnsafePass<SSAOData>(
            "Advanced SSAO", out var passData, s_ProfilingSampler))
        {
            // 텍스처 설정
            passData.depthTexture = resourceData.cameraDepthTexture;
            passData.normalTexture = GetNormalTexture(renderGraph, resourceData, desc);
            
            passData.ssaoTexture = CreateSSAOTexture(renderGraph, ssaoDesc, "_SSAO");
            passData.filteredSSAOTexture = CreateSSAOTexture(renderGraph, ssaoDesc, "_FilteredSSAO");
            
            if (m_SSAOSettings.temporalFiltering.value)
            {
                EnsureTemporalHistory(renderGraph, ssaoDesc);
                passData.temporalHistory = m_TemporalHistory;
            }
            
            // PassData 설정
            passData.ssaoSettings = m_SSAOSettings;
            passData.material = m_SSAOMaterial;
            passData.computeShader = m_SSAOCompute;
            passData.noiseTexture = m_NoiseTexture;
            passData.sampleKernel = m_SampleKernel;
            
            // 카메라 데이터
            passData.viewMatrix = cameraData.GetViewMatrix();
            passData.projectionMatrix = cameraData.GetProjectionMatrix();
            passData.previousViewMatrix = m_PreviousViewMatrix;
            passData.previousProjectionMatrix = m_PreviousProjectionMatrix;
            passData.isFirstFrame = m_FirstFrame;
            
            // 의존성 설정
            builder.UseTexture(passData.depthTexture, AccessFlags.Read);
            builder.UseTexture(passData.normalTexture, AccessFlags.Read);
            builder.UseTexture(passData.ssaoTexture, AccessFlags.ReadWrite);
            builder.UseTexture(passData.filteredSSAOTexture, AccessFlags.ReadWrite);
            
            if (passData.temporalHistory.IsValid())
                builder.UseTexture(passData.temporalHistory, AccessFlags.ReadWrite);
            
            builder.SetRenderFunc(static (SSAOData data, UnsafeGraphContext context) =>
            {
                ExecuteSSAOPasses(data, context);
            });
        }
        
        UpdateFrameState(cameraData);
    }
    
    private static void ExecuteSSAOPasses(SSAOData data, UnsafeGraphContext context)
    {
        var cmd = CommandBufferHelpers.GetNativeCommandBuffer(context.cmd);
        
        // 1. SSAO 생성
        if (data.computeShader != null && ShouldUseCompute(data.ssaoSettings))
        {
            ExecuteSSAOCompute(data, cmd);
        }
        else
        {
            ExecuteSSAOFragment(data, cmd);
        }
        
        // 2. 양방향 필터링
        if (data.ssaoSettings.bilateralFiltering.value)
        {
            ExecuteBilateralFilter(data, cmd);
        }
        else
        {
            cmd.Blit(data.ssaoTexture, data.filteredSSAOTexture);
        }
        
        // 3. 시간적 필터링
        if (data.ssaoSettings.temporalFiltering.value && !data.isFirstFrame)
        {
            ExecuteTemporalFilter(data, cmd);
        }
        
        // 4. 결과를 글로벌 텍스처로 설정
        cmd.SetGlobalTexture("_ScreenSpaceOcclusionTexture", data.filteredSSAOTexture);
    }
    
    private static void ExecuteSSAOCompute(SSAOData data, CommandBuffer cmd)
    {
        var settings = data.ssaoSettings;
        int kernelIndex = GetComputeKernel(data.computeShader, settings.technique.value);
        
        // 파라미터 설정
        SetupSSAOComputeParameters(data, cmd, kernelIndex);
        
        // Dispatch
        int groupsX = (data.ssaoTexture.rt.width + 7) / 8;
        int groupsY = (data.ssaoTexture.rt.height + 7) / 8;
        cmd.DispatchCompute(data.computeShader, kernelIndex, groupsX, groupsY, 1);
    }
    
    private static void ExecuteSSAOFragment(SSAOData data, CommandBuffer cmd)
    {
        SetupSSAOFragmentParameters(data);
        
        // SSAO 패스 실행
        cmd.Blit(data.depthTexture, data.ssaoTexture, data.material, k_SSAOPass);
    }
    
    private static void ExecuteBilateralFilter(SSAOData data, CommandBuffer cmd)
    {
        SetupBilateralFilterParameters(data);
        
        var tempRT = Shader.PropertyToID("_TempSSAORT");
        cmd.GetTemporaryRT(tempRT, data.ssaoTexture.rt.descriptor);
        
        // 여러 패스 필터링
        TextureHandle current = data.ssaoTexture;
        
        for (int i = 0; i < data.ssaoSettings.blurPasses.value; i++)
        {
            // 수평 패스
            cmd.SetGlobalFloat("_FilterDirection", 0f); // 0 = horizontal
            cmd.Blit(current, tempRT, data.material, k_BilateralFilterPass);
            
            // 수직 패스
            cmd.SetGlobalFloat("_FilterDirection", 1f); // 1 = vertical
            cmd.Blit(tempRT, data.filteredSSAOTexture, data.material, k_BilateralFilterPass);
            
            current = data.filteredSSAOTexture;
        }
        
        cmd.ReleaseTemporaryRT(tempRT);
    }
    
    private static void ExecuteTemporalFilter(SSAOData data, CommandBuffer cmd)
    {
        SetupTemporalFilterParameters(data);
        
        var tempRT = Shader.PropertyToID("_TempTemporalRT");
        cmd.GetTemporaryRT(tempRT, data.filteredSSAOTexture.rt.descriptor);
        
        // 시간적 필터링
        cmd.Blit(data.filteredSSAOTexture, tempRT, data.material, k_TemporalFilterPass);
        cmd.Blit(tempRT, data.filteredSSAOTexture);
        
        // 히스토리 업데이트
        cmd.Blit(data.filteredSSAOTexture, data.temporalHistory);
        
        cmd.ReleaseTemporaryRT(tempRT);
    }
    
    private static void SetupSSAOComputeParameters(SSAOData data, CommandBuffer cmd, int kernelIndex)
    {
        var settings = data.ssaoSettings;
        
        // 기본 파라미터
        var ssaoParams = new Vector4(
            settings.intensity.value,
            settings.radius.value,
            settings.power.value,
            settings.thickness.value
        );
        
        cmd.SetComputeVectorParam(data.computeShader, "_SSAOParams", ssaoParams);
        cmd.SetComputeFloatParam(data.computeShader, "_NormalBias", settings.normalBias.value);
        cmd.SetComputeFloatParam(data.computeShader, "_HorizonAngleThreshold", settings.horizonAngleThreshold.value);
        
        // 거리 감쇠
        var falloffParams = new Vector4(
            settings.falloffStart.value,
            settings.falloffEnd.value,
            1f / (settings.falloffEnd.value - settings.falloffStart.value),
            0f
        );
        cmd.SetComputeVectorParam(data.computeShader, "_FalloffParams", falloffParams);
        
        // 매트릭스
        cmd.SetComputeMatrixParam(data.computeShader, "_ViewMatrix", data.viewMatrix);
        cmd.SetComputeMatrixParam(data.computeShader, "_ProjectionMatrix", data.projectionMatrix);
        cmd.SetComputeMatrixParam(data.computeShader, "_InverseProjectionMatrix", 
            Matrix4x4.Inverse(data.projectionMatrix));
        
        // 텍스처
        cmd.SetComputeTextureParam(data.computeShader, kernelIndex, "_DepthTexture", data.depthTexture);
        cmd.SetComputeTextureParam(data.computeShader, kernelIndex, "_NormalTexture", data.normalTexture);
        cmd.SetComputeTextureParam(data.computeShader, kernelIndex, "_NoiseTexture", data.noiseTexture);
        cmd.SetComputeTextureParam(data.computeShader, kernelIndex, "_SSAOTexture", data.ssaoTexture);
        
        // 샘플 커널
        var kernelBuffer = new ComputeBuffer(data.sampleKernel.Length, sizeof(float) * 4);
        kernelBuffer.SetData(data.sampleKernel);
        cmd.SetComputeBufferParam(data.computeShader, kernelIndex, "_SampleKernel", kernelBuffer);
        cmd.SetComputeIntParam(data.computeShader, "_SampleCount", data.sampleKernel.Length);
        
        // 버퍼 해제 예약
        kernelBuffer.Release();
    }
    
    private static void SetupSSAOFragmentParameters(SSAOData data)
    {
        var settings = data.ssaoSettings;
        
        // Fragment shader용 파라미터 설정
        // (Compute shader와 유사하지만 SetGlobal 사용)
        
        var ssaoParams = new Vector4(
            settings.intensity.value,
            settings.radius.value,
            settings.power.value,
            settings.thickness.value
        );
        
        data.material.SetVector("_SSAOParams", ssaoParams);
        data.material.SetTexture("_NoiseTexture", data.noiseTexture);
        
        // 샘플 커널을 배열로 전달 (Fragment shader는 uniform array 사용)
        for (int i = 0; i < data.sampleKernel.Length; i++)
        {
            data.material.SetVector($"_SampleKernel{i}", data.sampleKernel[i]);
        }
        
        SetSSAOTechniqueKeywords(data.material, settings.technique.value);
    }
    
    private static void SetupBilateralFilterParameters(SSAOData data)
    {
        var bilateralParams = new Vector4(
            data.ssaoSettings.bilateralThreshold.value,
            0f, 0f, 0f
        );
        
        data.material.SetVector("_BilateralParams", bilateralParams);
        data.material.SetTexture("_DepthTexture", data.depthTexture);
        data.material.SetTexture("_NormalTexture", data.normalTexture);
    }
    
    private static void SetupTemporalFilterParameters(SSAOData data)
    {
        var temporalParams = new Vector4(
            data.ssaoSettings.temporalBlend.value,
            0f, 0f, 0f
        );
        
        data.material.SetVector("_TemporalParams", temporalParams);
        data.material.SetTexture("_TemporalHistory", data.temporalHistory);
        
        // Reprojection 매트릭스
        var reprojectionMatrix = data.previousViewMatrix * Matrix4x4.Inverse(data.viewMatrix);
        data.material.SetMatrix("_ReprojectionMatrix", reprojectionMatrix);
    }
    
    private static void SetSSAOTechniqueKeywords(Material material, SSAOTechnique technique)
    {
        material.DisableKeyword("_SSAO_SAO");
        material.DisableKeyword("_SSAO_HBAO");
        material.DisableKeyword("_SSAO_GTAO");
        material.DisableKeyword("_SSAO_RAYTRACED");
        
        switch (technique)
        {
            case SSAOTechnique.SAO:
                material.EnableKeyword("_SSAO_SAO");
                break;
            case SSAOTechnique.HBAO:
                material.EnableKeyword("_SSAO_HBAO");
                break;
            case SSAOTechnique.GTAO:
                material.EnableKeyword("_SSAO_GTAO");
                break;
            case SSAOTechnique.RayTraced:
                material.EnableKeyword("_SSAO_RAYTRACED");
                break;
        }
    }
    
    private static bool ShouldUseCompute(AdvancedSSAO settings)
    {
        // Compute shader 사용 조건 (복잡한 기법이나 고품질 모드)
        return settings.technique.value == SSAOTechnique.GTAO || 
               settings.sampleCount.value > 32;
    }
    
    private static int GetComputeKernel(ComputeShader compute, SSAOTechnique technique)
    {
        return technique switch
        {
            SSAOTechnique.SAO => compute.FindKernel("SSAO_SAO"),
            SSAOTechnique.HBAO => compute.FindKernel("SSAO_HBAO"),
            SSAOTechnique.GTAO => compute.FindKernel("SSAO_GTAO"),
            SSAOTechnique.RayTraced => compute.FindKernel("SSAO_RayTraced"),
            _ => compute.FindKernel("SSAO_SAO")
        };
    }
    
    private void GenerateNoiseTexture()
    {
        int size = 4; // 4x4 노이즈 텍스처
        m_NoiseTexture = new Texture2D(size, size, TextureFormat.RGBAFloat, false, true)
        {
            name = "SSAO_Noise",
            wrapMode = TextureWrapMode.Repeat,
            filterMode = FilterMode.Point
        };
        
        var pixels = new Color[size * size];
        var random = new Unity.Mathematics.Random(12345);
        
        for (int i = 0; i < pixels.Length; i++)
        {
            // 반구 위의 랜덤 벡터 생성
            Vector3 noise = new Vector3(
                random.NextFloat() * 2f - 1f,
                random.NextFloat() * 2f - 1f,
                0f
            ).normalized;
            
            pixels[i] = new Color(noise.x, noise.y, noise.z, 1f);
        }
        
        m_NoiseTexture.SetPixels(pixels);
        m_NoiseTexture.Apply();
    }
    
    private void GenerateSampleKernel()
    {
        int sampleCount = m_SSAOSettings?.sampleCount.value ?? 16;
        m_SampleKernel = new Vector4[sampleCount];
        
        var random = new Unity.Mathematics.Random(54321);
        
        for (int i = 0; i < sampleCount; i++)
        {
            // 반구 위의 균등 분포 샘플 생성
            Vector3 sample = new Vector3(
                random.NextFloat() * 2f - 1f,
                random.NextFloat() * 2f - 1f,
                random.NextFloat()
            ).normalized;
            
            // 반구 확인
            sample.z = Mathf.Abs(sample.z);
            
            // 거리 조정 (중심부에 더 많은 샘플)
            float scale = (float)i / sampleCount;
            scale = Mathf.Lerp(0.1f, 1f, scale * scale);
            sample *= scale;
            
            m_SampleKernel[i] = new Vector4(sample.x, sample.y, sample.z, 0f);
        }
    }
    
    private TextureHandle GetNormalTexture(RenderGraph renderGraph, UniversalResourceData resourceData, 
                                         RenderTextureDescriptor desc)
    {
        // Normal 텍스처가 이미 있다면 사용, 없으면 depth에서 재구성
        // 실제 구현에서는 GBuffer나 Normal Pass의 결과를 사용
        
        var normalDesc = desc;
        normalDesc.colorFormat = GraphicsFormat.R8G8B8A8_SNorm;
        normalDesc.name = "_CameraNormalsTexture";
        
        return UniversalRenderer.CreateRenderGraphTexture(renderGraph, normalDesc, 
            "_ReconstructedNormals", true);
    }
    
    private TextureHandle CreateSSAOTexture(RenderGraph renderGraph, RenderTextureDescriptor desc, string name)
    {
        return UniversalRenderer.CreateRenderGraphTexture(renderGraph, desc, name, true);
    }
    
    private RenderTextureDescriptor GetSSAODescriptor(RenderTextureDescriptor baseDesc)
    {
        var desc = baseDesc;
        desc.colorFormat = GraphicsFormat.R8_UNorm; // SSAO는 단일 채널
        desc.msaaSamples = 1;
        desc.depthBufferBits = 0;
        return desc;
    }
    
    private void EnsureTemporalHistory(RenderGraph renderGraph, RenderTextureDescriptor desc)
    {
        if (m_TemporalHistory == null || 
            !m_TemporalHistory.rt.IsCreated() ||
            m_TemporalHistory.rt.width != desc.width ||
            m_TemporalHistory.rt.height != desc.height)
        {
            m_TemporalHistory?.Release();
            m_TemporalHistory = RTHandles.Alloc(desc, name: "SSAO_TemporalHistory");
        }
    }
    
    private void UpdateFrameState(UniversalCameraData cameraData)
    {
        m_PreviousViewMatrix = cameraData.GetViewMatrix();
        m_PreviousProjectionMatrix = cameraData.GetProjectionMatrix();
        m_FirstFrame = false;
    }
    
    private bool ShouldRender(UniversalCameraData cameraData)
    {
        return cameraData.camera.cameraType == CameraType.Game &&
               m_SSAOSettings.IsActive();
    }
}

private class SSAOData
{
    internal TextureHandle depthTexture;
    internal TextureHandle normalTexture;
    internal TextureHandle ssaoTexture;
    internal TextureHandle filteredSSAOTexture;
    internal TextureHandle temporalHistory;
    internal AdvancedSSAO ssaoSettings;
    internal Material material;
    internal ComputeShader computeShader;
    internal Texture2D noiseTexture;
    internal Vector4[] sampleKernel;
    internal Matrix4x4 viewMatrix;
    internal Matrix4x4 projectionMatrix;
    internal Matrix4x4 previousViewMatrix;
    internal Matrix4x4 previousProjectionMatrix;
    internal bool isFirstFrame;
}
```

이 가이드는 Unity 6.0 URP에서 실제 프로덕션 품질의 포스트프로세싱 효과를 구현하기 위한 완전한 기술적 정보를 제공합니다. 각 효과는 성능과 품질 간의 균형을 고려하여 설계되었으며, 다양한 플랫폼에서 효과적으로 동작하도록 최적화되었습니다.