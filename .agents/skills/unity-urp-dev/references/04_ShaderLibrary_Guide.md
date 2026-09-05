# Unity 6.0 셰이더 라이브러리 활용 개발 가이드

## 개요

Unity 6.0의 셰이더 라이브러리 시스템을 활용하여 고품질의 RenderGraph 기반 포스트프로세싱 효과를 개발하기 위한 완전한 가이드입니다. 플랫폼 호환성부터 고급 최적화 기법까지, 실무에서 바로 활용할 수 있는 실용적인 정보를 제공합니다.

## 목차

1. [셰이더 라이브러리 기본 구조](#셰이더-라이브러리-기본-구조)
2. [플랫폼 호환성 시스템](#플랫폼-호환성-시스템)
3. [Core 수학 함수 활용](#core-수학-함수-활용)
4. [고급 샘플링 및 필터링](#고급-샘플링-및-필터링)
5. [색공간 변환 및 처리](#색공간-변환-및-처리)
6. [노이즈 및 랜덤 생성](#노이즈-및-랜덤-생성)
7. [Post-processing 특화 함수](#post-processing-특화-함수)
8. [Compute Shader 최적화](#compute-shader-최적화)
9. [디버깅 및 프로파일링](#디버깅-및-프로파일링)
10. [실전 구현 예제](#실전-구현-예제)

---

## 셰이더 라이브러리 기본 구조

### 필수 Include 헤더

#### 1. 기본 포스트프로세싱 셰이더 템플릿

> ⚠️ **템플릿 선택 기준**: URP RenderGraph에서 `Blitter.BlitTexture` / `Blitter.BlitCameraTexture`를 사용하는 경우 **반드시 Template B (Blit.hlsl)**를 사용한다. `Blitter`는 소스 텍스처를 `_BlitTexture`로 바인딩하므로, `_MainTex`를 선언한 셰이더에서는 소스를 읽지 못하고 화면이 흰색이 된다. Template A는 `cmd.SetGlobalTexture`로 직접 바인딩하거나 Blitter를 사용하지 않는 경우에만 사용한다.

**Template A — Blitter 미사용 (직접 바인딩)**

```hlsl
Shader "Hidden/CustomPostProcess"
{
    Properties
    {
        [HideInInspector] _MainTex ("Source Texture", 2D) = "white" {}
        [HideInInspector] _Intensity ("Effect Intensity", Float) = 1.0
    }
    
    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" }
        
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"
        #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Filtering.hlsl"
        #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Random.hlsl"
        
        // ⚠️ _MainTex: Blitter API와 함께 사용하면 소스를 읽지 못함
        // Blitter를 사용하지 않고 cmd.SetGlobalTexture로 직접 바인딩하는 경우에만 사용
        TEXTURE2D(_MainTex);
        SAMPLER(sampler_MainTex);
        float4 _MainTex_TexelSize;
        float _Intensity;
        
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
        
        Varyings vert(Attributes input)
        {
            Varyings output;
            UNITY_SETUP_INSTANCE_ID(input);
            UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(output);
            output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
            output.texcoord = input.texcoord;
            return output;
        }
        
        ENDHLSL
        
        Pass
        {
            Name "CustomPostProcess"
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            float4 frag(Varyings input) : SV_Target
            {
                UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input);
                float2 uv = input.texcoord;
                float4 color = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv);
                return color;
            }
            ENDHLSL
        }
    }
    FallBack "Hidden/Universal Render Pipeline/FallbackError"
}
```

**Template B — Blitter API 사용 (RenderGraph 표준, 권장)**

```hlsl
Shader "Hidden/CustomPostProcess_Blitter"
{
    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" }
        
        Pass
        {
            Name "CustomPostProcess"
            ZWrite Off ZTest Always Blend Off Cull Off
            
            HLSLPROGRAM
            #pragma vertex Vert       // Blit.hlsl 제공 full-screen triangle vertex
            #pragma fragment frag
            
            // Blit.hlsl: _BlitTexture, sampler_LinearClamp, Varyings, Vert 자동 선언
            #include "Packages/com.unity.render-pipelines.core/Runtime/Utilities/Blit.hlsl"
            #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"
            
            float _Intensity;
            
            half4 frag(Varyings input) : SV_Target
            {
                UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input);
                float2 uv = input.texcoord;
                // _BlitTexture: Blitter.BlitTexture가 소스를 바인딩하는 이름
                half4 color = SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_LinearClamp, uv);
                return color;
            }
            ENDHLSL
        }
    }
    FallBack "Hidden/Universal Render Pipeline/FallbackError"
}
```

#### 2. 라이브러리별 주요 기능

```hlsl
// === Core.hlsl ===
// - 플랫폼 추상화 (TEXTURE2D, SAMPLE_TEXTURE2D 등)
// - VR/XR 지원 (UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX)
// - 공간 변환 (TransformObjectToHClip, TransformWorldToView 등)

// === Color.hlsl ===
// - 색공간 변환 (SRGBToLinear, LinearToSRGB)
// - 휘도 계산 (Luminance)
// - 색온도 조정 (WhiteBalance)

// === Filtering.hlsl ===
// - 고급 필터링 (BicubicFilter, SampleTexture2DBiquadratic)
// - 업샘플링/다운샘플링

// === Random.hlsl ===
// - 해시 함수들 (Hash, JenkinsHash)
// - 노이즈 생성 (InterleavedGradientNoise)
```

---

## 플랫폼 호환성 시스템

### 플랫폼별 최적화 전략

#### 1. 모바일/데스크톱 분기 처리

```hlsl
#if SHADER_API_MOBILE
    // 모바일 최적화: half 정밀도 사용
    #define PRECISION half
    #define PRECISION2 half2
    #define PRECISION3 half3
    #define PRECISION4 half4
    
    // 간단한 샘플링
    #define SAMPLE_OPTIMIZED(tex, sampler, uv) SAMPLE_TEXTURE2D(tex, sampler, uv)
    
    // 저품질 필터
    #define USE_SIMPLE_FILTER 1
#else
    // 데스크톱: float 정밀도 사용
    #define PRECISION float
    #define PRECISION2 float2
    #define PRECISION3 float3
    #define PRECISION4 float4
    
    // 고품질 바이큐빅 샘플링
    #define SAMPLE_OPTIMIZED(tex, sampler, uv) SampleTexture2DBiquadratic(tex, sampler, uv, tex##_TexelSize)
    
    // 고품질 필터
    #define USE_SIMPLE_FILTER 0
#endif

// 사용 예제
float4 ApplyEffect(float2 uv)
{
    PRECISION4 color = SAMPLE_OPTIMIZED(_MainTex, sampler_MainTex, uv);
    
    #if USE_SIMPLE_FILTER
        // 모바일: 3x3 박스 필터
        return ApplySimpleFilter(uv, color);
    #else
        // 데스크톱: 고급 가우시안 필터
        return ApplyAdvancedFilter(uv, color);
    #endif
}
```

#### 2. API별 특화 최적화

```hlsl
// Vulkan 특화 서브패스 최적화
#if defined(SHADER_API_VULKAN) && defined(UNITY_FRAMEBUFFER_FETCH_AVAILABLE)
    #define USE_SUBPASS_INPUT 1
    FRAMEBUFFER_INPUT_X_FLOAT(0);
    
    float4 LoadFramebufferInput(float2 screenPos)
    {
        return LOAD_FRAMEBUFFER_INPUT_X(0, screenPos);
    }
#else
    #define USE_SUBPASS_INPUT 0
    
    float4 LoadFramebufferInput(float2 uv)
    {
        return SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv);
    }
#endif

// Metal 특화 최적화
#ifdef SHADER_API_METAL
    // Metal에서 더 효율적인 매드(MAD) 연산 사용
    #define FAST_MULTIPLY_ADD(a, b, c) mad(a, b, c)
#else
    #define FAST_MULTIPLY_ADD(a, b, c) ((a) * (b) + (c))
#endif

// D3D11/12 특화 Wave 연산
#if defined(SHADER_API_D3D11) || defined(SHADER_API_D3D12)
    #if defined(UNITY_PLATFORM_SUPPORTS_WAVE_32)
        #define WAVE_REDUCE_SUM(value) WaveActiveSum(value)
        #define WAVE_REDUCE_MAX(value) WaveActiveMax(value)
    #endif
#endif
```

#### 3. 조건부 컴파일 매크로 활용

```hlsl
// 품질별 다중 컴파일
#pragma multi_compile_local _ _QUALITY_LOW _QUALITY_MEDIUM _QUALITY_HIGH

float4 ApplyQualityBasedEffect(float2 uv)
{
    #if defined(_QUALITY_HIGH)
        // 고품질: 32 샘플 + 바이큐빅 필터링
        return ApplyHighQualityEffect(uv, 32);
    #elif defined(_QUALITY_MEDIUM)
        // 중품질: 16 샘플 + 바이리니어 필터링
        return ApplyMediumQualityEffect(uv, 16);
    #else
        // 저품질: 8 샘플 + 포인트 필터링
        return ApplyLowQualityEffect(uv, 8);
    #endif
}

// VR/XR 대응
#pragma multi_compile _ STEREO_INSTANCING_ON STEREO_MULTIVIEW_ON

float4 frag(Varyings input) : SV_Target
{
    UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input);
    
    // VR에서 올바른 눈의 텍스처 좌표 사용
    float2 uv = UnityStereoTransformScreenSpaceTex(input.texcoord);
    
    return ApplyEffect(uv);
}
```

---

## Core 수학 함수 활용

### 고성능 수학 연산 함수들

#### 1. 기본 수학 유틸리티

```hlsl
// Unity 제공 고성능 함수들
float3 color = float3(0.2, 0.7, 0.1);

// 최대/최소값 (GPU 최적화)
float maxComponent = Max3(color.r, color.g, color.b);
float minComponent = Min3(color.r, color.g, color.b);
float avgComponent = Avg3(color.r, color.g, color.b);

// 안전한 수학 연산 (NaN/Inf 방지)
float safeValue = IsFinite(someValue) ? someValue : 0.0;
color = any(IsNaN(color)) ? float3(0, 0, 0) : color;

// 빠른 정규화 (길이가 0이 아님을 보장할 때)
float3 normalizedFast = FastNormalize(someVector);

// 안전한 나눗셈
float safeDivision = SafeDiv(numerator, denominator); // 0으로 나누기 방지

// 포화(saturation) 연산 최적화
float saturated = FastSaturate(value); // [0,1] 클램핑

// 거듭제곱 최적화
float squared = Sq(value);           // value * value
float cubed = Cube(value);           // value * value * value
float pow4 = Pow4(value);            // 4제곱
float pow5 = Pow5(value);            // 5제곱
```

#### 2. 고급 보간 함수들

```hlsl
// 스무스스텝 변형들 (Unity 내장보다 더 부드러운 곡선)
float smoothstep5(float x) 
{
    x = saturate(x);
    return x * x * x * (x * (x * 6.0 - 15.0) + 10.0);
}

float smoothstep7(float x) 
{
    x = saturate(x);
    return x * x * x * x * (x * (x * (x * -20.0 + 70.0) - 84.0) + 35.0);
}

// 사용자 정의 easing 함수들
float easeInQuad(float t) { return t * t; }
float easeOutQuad(float t) { return t * (2.0 - t); }
float easeInOutQuad(float t) 
{
    return t < 0.5 ? 2.0 * t * t : -1.0 + (4.0 - 2.0 * t) * t;
}

float easeInCubic(float t) { return t * t * t; }
float easeOutCubic(float t) { return (--t) * t * t + 1.0; }

// 백 이징 (Back easing) - 오버슈트 효과
float easeInBack(float t)
{
    const float c1 = 1.70158;
    const float c3 = c1 + 1;
    return c3 * t * t * t - c1 * t * t;
}

// 탄성 이징 (Elastic easing)
float easeOutElastic(float t)
{
    const float c4 = (2 * PI) / 3;
    return t == 0 ? 0 : t == 1 ? 1 : pow(2, -10 * t) * sin((t * 10 - 0.75) * c4) + 1;
}

// 실사용 예제
float4 ApplyAnimatedEffect(float2 uv, float time)
{
    float4 color = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv);
    
    // 부드러운 페이드 인/아웃
    float fadeAmount = smoothstep5(sin(time * 2.0) * 0.5 + 0.5);
    
    // 탄성 있는 줌 효과
    float zoomFactor = 1.0 + easeOutElastic(fadeAmount) * 0.1;
    float2 centeredUV = (uv - 0.5) / zoomFactor + 0.5;
    
    return SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, centeredUV) * fadeAmount;
}
```

#### 3. 벡터 및 행렬 연산

```hlsl
// 고성능 행렬 연산
float4x4 CreateRotationMatrix(float3 axis, float angle)
{
    float c = cos(angle);
    float s = sin(angle);
    float t = 1.0 - c;
    
    axis = normalize(axis);
    
    return float4x4(
        t * axis.x * axis.x + c,          t * axis.x * axis.y - s * axis.z, t * axis.x * axis.z + s * axis.y, 0,
        t * axis.x * axis.y + s * axis.z, t * axis.y * axis.y + c,          t * axis.y * axis.z - s * axis.x, 0,
        t * axis.x * axis.z - s * axis.y, t * axis.y * axis.z + s * axis.x, t * axis.z * axis.z + c,          0,
        0,                                0,                                0,                                1
    );
}

// 쿼터니언 연산
float4 QuaternionMultiply(float4 q1, float4 q2)
{
    return float4(
        q1.w * q2.x + q1.x * q2.w + q1.y * q2.z - q1.z * q2.y,
        q1.w * q2.y - q1.x * q2.z + q1.y * q2.w + q1.z * q2.x,
        q1.w * q2.z + q1.x * q2.y - q1.y * q2.x + q1.z * q2.w,
        q1.w * q2.w - q1.x * q2.x - q1.y * q2.y - q1.z * q2.z
    );
}

float3 RotateVectorByQuaternion(float3 v, float4 q)
{
    float4 qv = float4(v, 0);
    float4 qconj = float4(-q.x, -q.y, -q.z, q.w);
    return QuaternionMultiply(QuaternionMultiply(q, qv), qconj).xyz;
}

// 구면 좌표계 변환
float3 SphericalToCartesian(float2 spherical) // (theta, phi)
{
    float sinTheta = sin(spherical.x);
    return float3(
        sinTheta * cos(spherical.y),
        cos(spherical.x),
        sinTheta * sin(spherical.y)
    );
}

float2 CartesianToSpherical(float3 cartesian)
{
    float theta = acos(cartesian.y);
    float phi = atan2(cartesian.z, cartesian.x);
    return float2(theta, phi);
}
```

---

## 고급 샘플링 및 필터링

### Unity 내장 고품질 필터링 함수 활용

#### 1. 바이큐빅 업샘플링

```hlsl
// Unity 내장 바이큐빅 샘플링 활용
#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Filtering.hlsl"

float4 SampleTexture2DHighQuality(TEXTURE2D_PARAM(tex, sampler_tex), float2 uv, float4 texelSize)
{
    // Unity의 고품질 바이큐빅 필터링
    return SampleTexture2DBicubic(TEXTURE2D_ARGS(tex, sampler_tex), uv, texelSize, 1.0, 0.0);
}

// B-Spline 필터 사용 (더욱 부드러운 결과)
float4 SampleTexture2DBSpline(TEXTURE2D_PARAM(tex, sampler_tex), float2 uv, float4 texelSize)
{
    // B-Spline 가중치 계산
    float2 weights[2];
    float2 offsets[2];
    BicubicFilter(frac(uv * texelSize.zw), weights, offsets);
    
    // 4-tap 샘플링
    float4 result = 0;
    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            float2 sampleUV = uv + (offsets[i].x * float2(1, 0) + offsets[j].y * float2(0, 1)) * texelSize.xy;
            result += SAMPLE_TEXTURE2D_LOD(tex, sampler_tex, sampleUV, 0) * weights[i].x * weights[j].y;
        }
    }
    
    return result;
}
```

#### 2. 고급 다운샘플링 기법

```hlsl
// 13-tap 다운샘플링 (Karis 평균)
float4 DownsampleKaris13Tap(TEXTURE2D_PARAM(tex, sampler_tex), float2 uv, float4 texelSize)
{
    float4 result = 0;
    
    // 중앙 샘플 (4배 가중치)
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv) * 4.0;
    
    // 십자가 패턴 (2배 가중치)
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2(-1,  0) * texelSize.xy) * 2.0;
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 1,  0) * texelSize.xy) * 2.0;
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 0, -1) * texelSize.xy) * 2.0;
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 0,  1) * texelSize.xy) * 2.0;
    
    // 대각선 패턴 (1배 가중치)
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2(-1, -1) * texelSize.xy);
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 1, -1) * texelSize.xy);
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2(-1,  1) * texelSize.xy);
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 1,  1) * texelSize.xy);
    
    // 외곽 십자가 (1배 가중치)
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2(-2,  0) * texelSize.xy);
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 2,  0) * texelSize.xy);
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 0, -2) * texelSize.xy);
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 0,  2) * texelSize.xy);
    
    return result / 16.0;
}

// 적응형 다운샘플링 (휘도 기반)
float4 DownsampleAdaptive(TEXTURE2D_PARAM(tex, sampler_tex), float2 uv, float4 texelSize)
{
    // 주변 9개 픽셀 샘플링
    float4 samples[9];
    float luminances[9];
    
    int index = 0;
    for (int y = -1; y <= 1; y++)
    {
        for (int x = -1; x <= 1; x++)
        {
            float2 sampleUV = uv + float2(x, y) * texelSize.xy;
            samples[index] = SAMPLE_TEXTURE2D(tex, sampler_tex, sampleUV);
            luminances[index] = Luminance(samples[index].rgb);
            index++;
        }
    }
    
    // 휘도 기반 가중 평균
    float4 result = 0;
    float totalWeight = 0;
    
    for (int i = 0; i < 9; i++)
    {
        float weight = 1.0 / (1.0 + luminances[i]); // 밝은 픽셀일수록 낮은 가중치
        result += samples[i] * weight;
        totalWeight += weight;
    }
    
    return result / totalWeight;
}
```

#### 3. 텐트 필터 업샘플링

```hlsl
// 9-tap 텐트 필터 (블룸 업샘플링에 이상적)
float4 UpsampleTent9Tap(TEXTURE2D_PARAM(tex, sampler_tex), float2 uv, float4 texelSize, float intensity)
{
    float4 result = 0;
    
    // 텐트 필터 가중치 패턴
    // 1 2 1
    // 2 4 2  
    // 1 2 1
    
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2(-1, -1) * texelSize.xy) * 1.0;
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 0, -1) * texelSize.xy) * 2.0;
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 1, -1) * texelSize.xy) * 1.0;
    
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2(-1,  0) * texelSize.xy) * 2.0;
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 0,  0) * texelSize.xy) * 4.0;
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 1,  0) * texelSize.xy) * 2.0;
    
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2(-1,  1) * texelSize.xy) * 1.0;
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 0,  1) * texelSize.xy) * 2.0;
    result += SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 1,  1) * texelSize.xy) * 1.0;
    
    return result * intensity / 16.0;
}

// 적응형 업샘플링 (에지 보존)
float4 UpsampleEdgePreserving(TEXTURE2D_PARAM(tex, sampler_tex), float2 uv, float4 texelSize)
{
    float4 center = SAMPLE_TEXTURE2D(tex, sampler_tex, uv);
    
    // 4방향 샘플
    float4 left   = SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2(-1,  0) * texelSize.xy);
    float4 right  = SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 1,  0) * texelSize.xy);
    float4 top    = SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 0, -1) * texelSize.xy);
    float4 bottom = SAMPLE_TEXTURE2D(tex, sampler_tex, uv + float2( 0,  1) * texelSize.xy);
    
    // 에지 감지 (휘도 차이 기반)
    float centerLum = Luminance(center.rgb);
    float leftLum = Luminance(left.rgb);
    float rightLum = Luminance(right.rgb);
    float topLum = Luminance(top.rgb);
    float bottomLum = Luminance(bottom.rgb);
    
    // 차이 기반 가중치 계산
    float leftWeight = 1.0 / (1.0 + abs(centerLum - leftLum));
    float rightWeight = 1.0 / (1.0 + abs(centerLum - rightLum));
    float topWeight = 1.0 / (1.0 + abs(centerLum - topLum));
    float bottomWeight = 1.0 / (1.0 + abs(centerLum - bottomLum));
    
    float totalWeight = leftWeight + rightWeight + topWeight + bottomWeight;
    
    return (left * leftWeight + right * rightWeight + top * topWeight + bottom * bottomWeight) / totalWeight;
}
```

---

## 색공간 변환 및 처리

### 고급 색상 처리 함수들

#### 1. HSV 색공간 활용

```hlsl
#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"

// 확장된 HSV 함수들 (Unity 내장 함수 활용)
float3 AdjustHue(float3 color, float hueShift)
{
    float3 hsv = RgbToHsv(color);
    hsv.x = frac(hsv.x + hueShift);
    return HsvToRgb(hsv);
}

float3 AdjustSaturation(float3 color, float saturation)
{
    float3 hsv = RgbToHsv(color);
    hsv.y = saturate(hsv.y * saturation);
    return HsvToRgb(hsv);
}

float3 AdjustValue(float3 color, float value)
{
    float3 hsv = RgbToHsv(color);
    hsv.z = saturate(hsv.z * value);
    return HsvToRgb(hsv);
}

// 선택적 색상 조정 (특정 색상 범위만 조정)
float3 AdjustSelectiveColor(float3 color, float3 targetHue, float range, float hueShift, float satShift, float valShift)
{
    float3 hsv = RgbToHsv(color);
    
    // 목표 색상과의 거리 계산 (색조 공간에서 순환 거리)
    float hueDist = min(abs(hsv.x - targetHue.x), 1.0 - abs(hsv.x - targetHue.x));
    float mask = smoothstep(range, range * 0.5, hueDist);
    
    // 마스크를 적용한 조정
    hsv.x = frac(hsv.x + hueShift * mask);
    hsv.y = saturate(hsv.y * (1.0 + satShift * mask));
    hsv.z = saturate(hsv.z * (1.0 + valShift * mask));
    
    return HsvToRgb(hsv);
}
```

#### 2. 색온도 및 화이트 밸런스

```hlsl
// 정확한 색온도 변환 (Kelvin to RGB)
float3 KelvinToRGB(float temperature)
{
    // 1000K ~ 40000K 범위 지원
    temperature = clamp(temperature, 1000, 40000) / 100.0;
    
    float3 color;
    
    // 빨간색 성분
    if (temperature <= 66.0)
        color.r = 1.0;
    else
        color.r = saturate((329.698727446 * pow(temperature - 60.0, -0.1332047592)) / 255.0);
    
    // 녹색 성분
    if (temperature <= 66.0)
        color.g = saturate((99.4708025861 * log(temperature) - 161.1195681661) / 255.0);
    else
        color.g = saturate((288.1221695283 * pow(temperature - 60.0, -0.0755148492)) / 255.0);
    
    // 파란색 성분
    if (temperature >= 66.0)
        color.b = 1.0;
    else if (temperature <= 19.0)
        color.b = 0.0;
    else
        color.b = saturate((138.5177312231 * log(temperature - 10.0) - 305.0447927307) / 255.0);
    
    return color;
}

// 화이트 밸런스 조정
float3 ApplyWhiteBalance(float3 color, float temperature, float tint)
{
    // 색온도를 RGB로 변환
    float3 temperatureRGB = KelvinToRGB(temperature);
    
    // 틴트 적용 (마젠타-그린 축)
    float3 tintRGB = lerp(float3(1, 1 - tint * 0.1, 1 - tint * 0.2), 
                         float3(1 - tint * 0.1, 1, 1 - tint * 0.1), 
                         step(0, tint));
    
    return color * temperatureRGB * tintRGB;
}
```

#### 3. 고급 색상 그레이딩

```hlsl
// Shadow/Midtone/Highlight 분리 조정
float3 ShadowMidtoneHighlight(float3 color, float3 shadowColor, float3 midtoneColor, float3 highlightColor)
{
    float luminance = Luminance(color);
    
    // 영역별 마스크 생성 (부드러운 전환)
    float shadowMask = 1.0 - smoothstep(0.0, 0.5, luminance);
    float highlightMask = smoothstep(0.5, 1.0, luminance);
    float midtoneMask = 1.0 - shadowMask - highlightMask;
    
    // 각 영역별 색상 조정 적용
    float3 adjustedShadow = color * shadowColor;
    float3 adjustedMidtone = color * midtoneColor;
    float3 adjustedHighlight = color * highlightColor;
    
    return adjustedShadow * shadowMask + 
           adjustedMidtone * midtoneMask + 
           adjustedHighlight * highlightMask;
}

// 색상 룩업 테이블 (LUT) 적용
float3 ApplyLUT(float3 color, TEXTURE2D_PARAM(lutTex, sampler_lutTex), float lutSize, float contribution)
{
    // 3D LUT를 2D 텍스처로 저장된 경우의 샘플링
    color = saturate(color);
    
    float3 lutST = color * (lutSize - 1.0);
    float3 lutST_floor = floor(lutST);
    float3 lutST_frac = lutST - lutST_floor;
    
    // 8개 모서리 샘플링을 위한 좌표 계산
    float slice = lutST_floor.z;
    float sliceNext = min(slice + 1.0, lutSize - 1.0);
    
    float2 uv1 = float2(lutST_floor.x + slice * lutSize, lutST_floor.y) / (lutSize * lutSize);
    float2 uv2 = float2(lutST_floor.x + 1.0 + slice * lutSize, lutST_floor.y) / (lutSize * lutSize);
    float2 uv3 = float2(lutST_floor.x + slice * lutSize, lutST_floor.y + 1.0) / (lutSize * lutSize);
    float2 uv4 = float2(lutST_floor.x + 1.0 + slice * lutSize, lutST_floor.y + 1.0) / (lutSize * lutSize);
    
    float2 uv5 = float2(lutST_floor.x + sliceNext * lutSize, lutST_floor.y) / (lutSize * lutSize);
    float2 uv6 = float2(lutST_floor.x + 1.0 + sliceNext * lutSize, lutST_floor.y) / (lutSize * lutSize);
    float2 uv7 = float2(lutST_floor.x + sliceNext * lutSize, lutST_floor.y + 1.0) / (lutSize * lutSize);
    float2 uv8 = float2(lutST_floor.x + 1.0 + sliceNext * lutSize, lutST_floor.y + 1.0) / (lutSize * lutSize);
    
    // 3D 보간
    float3 sample1 = SAMPLE_TEXTURE2D_LOD(lutTex, sampler_lutTex, uv1, 0).rgb;
    float3 sample2 = SAMPLE_TEXTURE2D_LOD(lutTex, sampler_lutTex, uv2, 0).rgb;
    float3 sample3 = SAMPLE_TEXTURE2D_LOD(lutTex, sampler_lutTex, uv3, 0).rgb;
    float3 sample4 = SAMPLE_TEXTURE2D_LOD(lutTex, sampler_lutTex, uv4, 0).rgb;
    float3 sample5 = SAMPLE_TEXTURE2D_LOD(lutTex, sampler_lutTex, uv5, 0).rgb;
    float3 sample6 = SAMPLE_TEXTURE2D_LOD(lutTex, sampler_lutTex, uv6, 0).rgb;
    float3 sample7 = SAMPLE_TEXTURE2D_LOD(lutTex, sampler_lutTex, uv7, 0).rgb;
    float3 sample8 = SAMPLE_TEXTURE2D_LOD(lutTex, sampler_lutTex, uv8, 0).rgb;
    
    float3 slice1 = lerp(lerp(sample1, sample2, lutST_frac.x), lerp(sample3, sample4, lutST_frac.x), lutST_frac.y);
    float3 slice2 = lerp(lerp(sample5, sample6, lutST_frac.x), lerp(sample7, sample8, lutST_frac.x), lutST_frac.y);
    
    float3 result = lerp(slice1, slice2, lutST_frac.z);
    
    return lerp(color, result, contribution);
}
```

---

## 노이즈 및 랜덤 생성

### Unity 내장 노이즈 함수 활용

#### 1. 기본 노이즈 생성

```hlsl
#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Random.hlsl"

// Unity 제공 고품질 노이즈 함수들
float GenerateNoise(float2 uv, float time)
{
    // Interleaved Gradient Noise (IGN) - 고품질, 빠른 속도
    return InterleavedGradientNoise(uv * _ScreenParams.xy, time * 1000.0);
}

// 해시 기반 랜덤 (일관성 있는 랜덤)
float HashRandom(uint seed)
{
    return Hash(seed);
}

// 시간 기반 애니메이션 노이즈
float AnimatedNoise(float2 uv, float time, float scale)
{
    float2 scaledUV = uv * scale;
    float noise1 = InterleavedGradientNoise(scaledUV, time);
    float noise2 = InterleavedGradientNoise(scaledUV * 2.17, time * 1.33);
    return (noise1 + noise2 * 0.5) / 1.5;
}
```

#### 2. 커스텀 고급 노이즈 함수

```hlsl
// Perlin 노이즈 구현
float2 Random2D(float2 st) 
{
    st = float2(dot(st, float2(127.1, 311.7)), dot(st, float2(269.5, 183.3)));
    return -1.0 + 2.0 * frac(sin(st) * 43758.5453123);
}

float PerlinNoise(float2 st) 
{
    float2 i = floor(st);
    float2 f = frac(st);
    
    float2 u = f * f * (3.0 - 2.0 * f); // 에르미트 곡선
    
    return lerp(lerp(dot(Random2D(i + float2(0.0, 0.0)), f - float2(0.0, 0.0)),
                     dot(Random2D(i + float2(1.0, 0.0)), f - float2(1.0, 0.0)), u.x),
                lerp(dot(Random2D(i + float2(0.0, 1.0)), f - float2(0.0, 1.0)),
                     dot(Random2D(i + float2(1.0, 1.0)), f - float2(1.0, 1.0)), u.x), u.y);
}

// Fractal Brownian Motion (fBm) - 여러 옥타브 노이즈
float fBmNoise(float2 st, int octaves, float lacunarity, float gain)
{
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    
    for (int i = 0; i < octaves; i++) 
    {
        value += amplitude * PerlinNoise(st * frequency);
        st *= lacunarity;
        amplitude *= gain;
    }
    return value;
}

// Simplex 노이즈 (더 자연스러운 패턴)
float3 mod289(float3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
float2 mod289_2(float2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
float3 permute(float3 x) { return mod289(((x * 34.0) + 1.0) * x); }

float SimplexNoise(float2 v)
{
    const float4 C = float4(0.211324865405187,  // (3.0-sqrt(3.0))/6.0
                           0.366025403784439,   // 0.5*(sqrt(3.0)-1.0)
                          -0.577350269189626,   // -1.0 + 2.0 * C.x
                           0.024390243902439);  // 1.0 / 41.0

    float2 i = floor(v + dot(v, C.yy));
    float2 x0 = v - i + dot(i, C.xx);

    float2 i1;
    i1 = (x0.x > x0.y) ? float2(1.0, 0.0) : float2(0.0, 1.0);
    float4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;

    i = mod289_2(i);
    float3 p = permute(permute(i.y + float3(0.0, i1.y, 1.0)) + i.x + float3(0.0, i1.x, 1.0));

    float3 m = max(0.5 - float3(dot(x0, x0), dot(x12.xy, x12.xy), dot(x12.zw, x12.zw)), 0.0);
    m = m * m;
    m = m * m;

    float3 x = 2.0 * frac(p * C.www) - 1.0;
    float3 h = abs(x) - 0.5;
    float3 ox = floor(x + 0.5);
    float3 a0 = x - ox;

    m *= 1.79284291400159 - 0.85373472095314 * (a0 * a0 + h * h);

    float3 g;
    g.x = a0.x * x0.x + h.x * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;
    return 130.0 * dot(m, g);
}
```

#### 3. 특수 노이즈 패턴

```hlsl
// Worley 노이즈 (셀룰러 노이즈)
float WorleyNoise(float2 uv, float scale)
{
    float2 scaledUV = uv * scale;
    float2 i_st = floor(scaledUV);
    float2 f_st = frac(scaledUV);
    
    float minDist = 1.0;
    
    for (int y = -1; y <= 1; y++) 
    {
        for (int x = -1; x <= 1; x++) 
        {
            float2 neighbor = float2(float(x), float(y));
            float2 point = Random2D(i_st + neighbor);
            point = 0.5 + 0.5 * sin(point * 6.2831853);
            
            float2 diff = neighbor + point - f_st;
            float dist = length(diff);
            
            minDist = min(minDist, dist);
        }
    }
    
    return minDist;
}

// 리지 노이즈 (산맥 같은 패턴)
float RidgeNoise(float2 st, int octaves)
{
    float value = 0.0;
    float amplitude = 0.5;
    
    for (int i = 0; i < octaves; i++) 
    {
        float n = abs(PerlinNoise(st));
        n = 1.0 - n; // 역전
        n = n * n;   // 제곱으로 예리하게
        
        value += n * amplitude;
        st *= 2.0;
        amplitude *= 0.5;
    }
    
    return value;
}

// 터불런스 노이즈
float TurbulenceNoise(float2 st, int octaves)
{
    float value = 0.0;
    float amplitude = 0.5;
    
    for (int i = 0; i < octaves; i++) 
    {
        value += abs(PerlinNoise(st)) * amplitude;
        st *= 2.0;
        amplitude *= 0.5;
    }
    
    return value;
}
```

---

## HLSL 흐름 제어 최적화 Attribute

### 개요

HLSL에는 반복문과 조건문의 컴파일/실행 방식을 제어하는 네 가지 attribute가 있다.
Unity는 이를 `HLSLSupport.cginc`에서 플랫폼 매크로로 래핑한다.

**Unity 매크로 매핑 (HLSLSupport.cginc)**

```hlsl
// UNITY_COMPILER_HLSL (DirectX, Metal, Vulkan 등 HLSLcc 경로)일 때:
#define UNITY_BRANCH    [branch]
#define UNITY_FLATTEN   [flatten]
#define UNITY_UNROLL    [unroll]
#define UNITY_LOOP      [loop]

// 그 외 플랫폼(구형 OpenGL ES 등)에서는 빈 매크로로 처리됨 — 무시됨
```

Metal/Vulkan/OpenGLES3는 모두 HLSLcc 경로를 사용하므로 모바일에서도 동작한다.
단, 빈 매크로 폴백이 있어 컴파일 오류 없이 묵시적으로 무시될 수 있다는 점을 인지해야 한다.

---

### [loop] vs [unroll] — 반복문

#### 개념

| Attribute | 컴파일러 동작 | 결과 |
|-----------|--------------|------|
| `[unroll]` | 루프를 정적으로 전개 — 반복 횟수만큼 명령어 복제 | 분기 명령어 제거, 컴파일 시 모든 경로 확정 |
| `[loop]` | 동적 루프 유지 — 카운터·점프 명령어 삽입 | 런타임 조건으로 반복 횟수 결정 가능 |

컴파일러는 기본적으로 반복 횟수를 컴파일 타임에 알 수 있으면 unroll, 그렇지 않으면 loop를 선택한다.
attribute는 이 기본 동작을 명시적으로 **강제**한다.

#### 선택 기준

| 조건 | 권장 |
|------|------|
| 반복 횟수가 상수이고 작다 (≤8) | `[unroll]` |
| 반복 횟수가 상수이고 크다 (>16) | `[loop]` — 코드 팽창 방지 |
| 반복 횟수가 런타임 변수 (cbuffer, 텍스처 값) | `[loop]` 필수 |
| 루프 내부에서 일찍 종료(`break`)가 잦음 | `[loop]` — 조기 탈출 이득 |
| 루프 내부에서 `Sample()` 사용 | `[unroll]` — gradient 연산 허용 |
| 루프 내부에서 `SampleLevel()` / `SampleGrad()` 사용 | `[loop]` 가능 |

**핵심 제약**: `[loop]`(동적 루프) 내부에서 암묵적 LOD를 사용하는 `Sample()`/`tex2D()` 호출은 **컴파일 오류**를 발생시킨다. GPU가 2×2 픽셀 그룹 간 gradient를 계산할 수 없기 때문이다. 대안은 `SampleLevel()` 또는 `SampleGrad()`다.

#### 코드 예시

```hlsl
// 상수 횟수 — unroll이 유리 (분기 명령어 없음)
[unroll]
for (int i = 0; i < 4; i++)
{
    result += SAMPLE_TEXTURE2D_LOD(_MainTex, sampler_MainTex, uv + offsets[i], 0);
}

// 런타임 변수 횟수 — loop 필수
int sampleCount = (int)_SampleCount; // cbuffer에서 오는 값
[loop]
for (int i = 0; i < sampleCount; i++)
{
    // Sample() 사용 불가 — SampleLevel()로 대체
    result += SAMPLE_TEXTURE2D_LOD(_MainTex, sampler_MainTex, uv + offsets[i], mipLevel);
}

// Unity 매크로 사용 (플랫폼 호환)
UNITY_LOOP
for (int i = 0; i < _DynamicCount; i++)
{
    result += ComputeSample(uv, i);
}

UNITY_UNROLL
for (int i = 0; i < 8; i++)
{
    result += kernel[i] * SAMPLE_TEXTURE2D_LOD(_BlurTex, sampler_BlurTex, uv + dir * i, 0);
}

// 최대 횟수를 명시하여 unroll (런타임 값이지만 상한이 알려진 경우)
[unroll(8)]
for (int i = 0; i < count; i++) // count <= 8 보장
{
    result += weights[i] * samples[i];
}
```

#### 모바일 GPU 주의사항 (Mali/Adreno)

**Mali (TBDR 아키텍처)**
- Mali는 SIMD 벡터 코어를 사용하며 in-order 실행이 많다. 루프 언롤로 명령어 ILP(명령어 수준 병렬성)를 높이면 유리하다.
- 그러나 언롤로 셰이더 코드 크기가 커지면 명령어 캐시 압박이 생겨 오히려 역효과를 낼 수 있다. 반복 횟수 8 초과 시 주의.
- Mali에서는 루프 변수를 `mediump`가 아닌 `int`로 유지해야 한다 — 정밀도 강등이 카운터 오동작을 유발할 수 있다.

**Adreno (Qualcomm)**
- Adreno는 동적 분기 성능이 비교적 양호하다. 반복 횟수가 런타임 변수라면 `[loop]`가 코드 팽창 없이 좋은 선택이다.
- 루프 내부 텍스처 의존 읽기(texture-dependent read)는 파이프라인 지연을 유발한다. 가능하면 루프 외부에서 좌표를 미리 계산한다.

---

### [branch] vs [flatten] — 조건문

#### 개념

| Attribute | 컴파일러 동작 | 실행 방식 |
|-----------|--------------|----------|
| `[flatten]` | 조건문을 평탄화 — 분기 명령어 없음 | 양쪽 블록을 모두 실행 후 `select` 명령으로 결과 선택 |
| `[branch]` | 실제 분기 명령어 삽입 | 조건에 따라 한쪽 블록만 실행 |

#### Uniform vs Divergent Flow Control

- **Uniform flow control**: 같은 draw call의 모든 픽셀(wave/wavefront)이 동일한 분기 경로를 취하는 경우. `[branch]`가 효율적 — GPU 전체가 한 경로만 실행.
- **Divergent flow control**: 같은 wave 내 픽셀들이 서로 다른 경로를 취하는 경우. `[branch]`를 써도 wave가 분리되거나 비활성 레인이 생겨 오버헤드 발생. `[flatten]`이 더 안전할 수 있음.

#### 선택 기준

| 조건 | 권장 |
|------|------|
| 조건이 상수 또는 cbuffer 값 (uniform) | `[branch]` — 비용 없는 전체 경로 스킵 |
| 조건이 픽셀마다 다른 값 (텍스처 샘플 결과 등) | `[flatten]` — divergent branch 오버헤드 회피 |
| 분기 내 비용이 매우 크고 실제로 스킵 가능성 높음 | `[branch]` |
| 분기 내 비용이 작고 양쪽 코드가 비슷한 길이 | `[flatten]` |
| 분기 내부에 `Sample()` 사용 (gradient 의존) | `[flatten]` 또는 분기 전에 gradient 계산 후 `SampleGrad()` 사용 |
| Framebuffer fetch / 타일 메모리 연산 포함 | `[flatten]` 금지 — 반드시 `[branch]` 사용 |

**Framebuffer fetch와 `[flatten]` 충돌**

타일 메모리 읽기(Vulkan subpass input, Metal framebuffer fetch)는 GPU 타일 내에서 현재 픽셀의 프레임버퍼 값을 직접 읽는다. `[flatten]`은 조건이 false여도 블록을 실행하기 때문에 타일 메모리 접근이 의도치 않게 발생할 수 있다. 이는 잘못된 결과나 드라이버 수준의 undefined behavior로 이어진다. Framebuffer fetch가 포함된 조건문에는 반드시 `[branch]`를 사용한다.

#### 코드 예시

```hlsl
// cbuffer uniform 조건 — branch가 유리 (전체 픽셀이 동일한 경로)
UNITY_BRANCH
if (_EnableEffect > 0.5)
{
    // 비용이 큰 연산 — 비활성화 시 완전히 스킵됨
    result = ApplyExpensiveEffect(uv, result);
}

// 텍스처 기반 조건 — flatten이 안전 (픽셀마다 값이 다름)
UNITY_FLATTEN
if (mask > 0.5)
{
    result = ApplyEffect(result);
}

// Framebuffer fetch를 포함한 조건 — 반드시 branch
UNITY_BRANCH
if (needsBlend)
{
    // Vulkan subpass input 또는 Metal framebuffer fetch
    float4 prevColor = LOAD_FRAMEBUFFER_INPUT(0);
    result = lerp(prevColor, result, blendFactor);
}

// gradient 의존 샘플링 — flatten 내부에서도 가능하지 않은 경우: SampleGrad 사용
float2 dx = ddx(uv);
float2 dy = ddy(uv);

UNITY_BRANCH
if (condition)
{
    // branch 내부에서 gradient 사용 시 — gradient를 branch 밖에서 계산하고 SampleGrad 사용
    result = SAMPLE_TEXTURE2D_GRAD(_Tex, sampler_Tex, uv, dx, dy);
}
```

#### 모바일 GPU 주의사항 (Mali/Adreno)

**Mali**
- Mali는 predicated execution(조건부 실행)을 지원하여 단순한 분기는 `[flatten]`과 유사하게 양쪽 실행 후 선택한다. 조건이 uniform에 가까울수록 `[branch]`가 유리하다.
- 모바일 포스트프로세싱에서 framebuffer fetch를 활용할 때 `[branch]` + uniform 조건 조합이 대역폭을 크게 절약한다.

**Adreno**
- Adreno는 wavefront 단위로 분기를 처리한다. Divergent branch는 wave를 분할하거나 비활성 레인을 포함한 채 양 경로를 실행해 효율이 저하된다.
- 조건이 텍스처 룩업 결과인 경우 `[flatten]`으로 명시적으로 평탄화하면 wave 분할 오버헤드를 없앨 수 있다.

---

### 실무 판단 체크리스트

```
반복문 작성 시:
  반복 횟수가 컴파일 타임에 확정되는가?
    Yes → 횟수가 ≤8인가?
      Yes → [unroll] 사용
      No  → [loop] 사용 (코드 팽창 방지)
    No  → [loop] 사용 (UNITY_LOOP)
  루프 내부에서 Sample() 사용하는가?
    [loop] 내부에서는 사용 불가 → SampleLevel() / SampleGrad() 로 대체

조건문 작성 시:
  조건 값이 draw call 전체에서 동일한가 (cbuffer, material property)?
    Yes → [branch] 사용 (UNITY_BRANCH) — 비용 큰 코드 완전 스킵
    No  → 픽셀마다 다른 값 (텍스처 샘플 등)?
      Yes → [flatten] 사용 (UNITY_FLATTEN) — wave 분기 방지
  조건 블록 내부에 framebuffer fetch / subpass input 읽기가 있는가?
    Yes → 반드시 [branch] 사용
  조건 블록 내부에 Sample() (암묵적 gradient)가 있는가?
    [branch] 내부: branch 밖에서 ddx/ddy 미리 계산 후 SampleGrad() 사용
    [flatten] 내부: 직접 Sample() 사용 가능 (양쪽 모두 실행되므로 gradient 유효)
```

---

이 가이드는 Unity 6.0 셰이더 라이브러리의 핵심 기능들을 실무에서 바로 활용할 수 있도록 구성했습니다. 다음 섹션에서는 Post-processing 특화 함수들과 Compute Shader 최적화에 대해 계속 다루겠습니다.