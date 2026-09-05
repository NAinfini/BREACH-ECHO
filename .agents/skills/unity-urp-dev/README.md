<div align="center">

# 🎮 claude-skill-unity-urp

**Unity URP RenderGraph 기반 렌더피쳐 개발을 위한 Claude Code 스킬**

[![Unity](https://img.shields.io/badge/Unity-6000.x-black?style=flat-square&logo=unity)](https://unity.com)
[![URP](https://img.shields.io/badge/URP-17.x-blue?style=flat-square)](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.3)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-orange?style=flat-square)](https://claude.ai/code)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**Language / 언어**  
[![한국어](https://img.shields.io/badge/🇰🇷_한국어-현재_문서-red?style=flat-square)](#korean) [![English](https://img.shields.io/badge/🇺🇸_English-available-blue?style=flat-square)](#english)

</div>

---

<a name="korean"></a>

## 소개

`unity-urp-dev`는 Unity URP RenderGraph 기반 렌더피쳐 개발 시 Claude Code가 올바른 방향으로 코드를 생성하도록 안내하는 스킬입니다.

이 스킬의 핵심은 두 가지입니다.

**1. 고급 렌더링 기법 레퍼런스**  
`references/` 폴더에는 RenderGraph API 패턴, Job System / Burst 컴파일러, Compute Shader, unsafe zero-copy 메모리 전송 등 실전 구현에 필요한 고급 기법이 문서화되어 있습니다. Claude Code가 이 레퍼런스를 직접 읽고 검증된 패턴으로 코드를 작성합니다.

**2. URP 버전 인식 코드 생성**  
스킬은 작업 시작 전 프로젝트의 URP 버전을 자동으로 감지합니다. 감지된 버전에 맞는 공식 Unity Docs와 URP GitHub 소스를 참조하여, 버전별 API 차이로 인한 오류를 사전에 방지합니다.

<img width="1229" height="671" alt="image" src="https://github.com/user-attachments/assets/d5da7338-b14d-404c-aa38-212e885ce747" />


### 적용 영역

| 키워드 | 내용 |
|---|---|
| `RenderGraph` | `AddRasterRenderPass`, `AddUnsafePass`, `AddComputePass` 패턴 |
| `RendererFeature` | `ScriptableRendererFeature` 전체 구조 및 Volume 통합 |
| `PostProcessing` | Bloom, DoF, Motion Blur, SSAO, TAA, 커스텀 이펙트 |
| `HLSL / ShaderLibrary` | `Blit.hlsl`, 수학 함수, 색공간 변환, 모바일 정밀도 |
| `Compute Shader` | Compute Pass, AsyncGPUReadback, GPU Culling |
| `Unity 6.0` | GPU Resident Drawer, RenderGraph Viewer 디버깅 |

---

## 설치

### 수동 설치

```bash
# 1. Claude Code 스킬 디렉토리로 이동
cd ~/.claude/skills

# 2. 저장소 클론
git clone https://github.com/CatDarkGame/claude-skill-unity-urp unity-urp-dev
```

설치 후 Claude Code에서 URP 관련 작업 시 자동으로 스킬이 활성화됩니다.

### 활성화 트리거

URP RenderGraph 및 렌더피쳐 개발과 관련된 키워드 등이 대화에 등장하면 스킬이 자동 로드됩니다. Claude Code가 대화에서 관련 키워드를 감지하면 `SKILL.md`의 description과 매칭하여 스킬 컨텍스트를 로드합니다.

`URP` · `RenderGraph` · `RendererFeature` · `ScriptableRenderPass` · `PostProcess` · `HLSL` · `SSR` · `Bloom` · `DoF` · `TAA` · `Compute Shader` · `Burst` · `Job System` · 등

---

## 스킬 구성

```
unity-urp-dev/
├── SKILL.md                              # 스킬 진입점 (버전 감지 → 레퍼런스 라우팅)
└── references/
    ├── 01_URP_Core_Package_Guide.md      # RenderGraph 핵심 패스 구조
    ├── 02_RenderPipelineCore_Guide.md    # Volume System, VolumeComponent
    ├── 03_PostProcessing_Effects_Guide.md # Bloom, DoF, TAA, SSAO 구현
    ├── 04_ShaderLibrary_Guide.md         # HLSL, ShaderLibrary, 샘플링 패턴
    ├── 05_Mathematics_Collections_Guide.md # Unity.Mathematics, Burst, Job System
    ├── 06_Unity60_NewFeatures_Guide.md   # Unity 6.0 신기능
    ├── 07_Advanced_Memory_Management_Guide.md # Constant Buffer, GPU 메모리
    └── 08_Compute_Shader_Integration_Guide.md # Compute Pass, GPU Culling
```

스킬의 첫 단계는 프로젝트의 URP 버전을 자동 감지하는 것입니다. API는 버전마다 다르기 때문에, 버전 확인 없이 코드 생성을 시작하지 않습니다.

---

## 검증: 스킬 유무 비교

> **테스트 환경:** Unity 6000.3.10f1 / URP 17.3.0  
> **구현 대상:** Radial Blur 포스트프로세싱 이펙트  
> **비교 방법:** 동일한 기능 요구사항으로 스킬 유무에 따라 각각 독립 구현

<img width="1125" height="634" alt="image" src="https://github.com/user-attachments/assets/58fac3f7-3d01-4f48-bfc4-952c525aee59" />


### 요약

| # | 검증 항목 | WITH skill | WITHOUT skill | 실제 영향 |
|---|---|:---:|:---:|---|
| 1 | URP 17 RenderGraph 친화성 | ✅ | ❌ | RenderGraph Validator 경고 발생 |
| 2 | 모바일 성능 최적화 | ✅ | ❌ | GPU 비용 ~20-35% 증가 |
| 3 | Volume System 통합 | ✅ | ❌ | 씬 파라미터 블렌딩 불가 |
| 4 | CBUFFER 타입 안전성 | ✅ | ❌ | Metal/Vulkan 에서 잠재 버그 |
| 5 | Blitter API 정합성 | ✅ | ❌ | API 교체 시 화면 전체 흰색 |

---

### 검증 1 — RenderGraph API 선택

`AddRasterRenderPass`와 `AddUnsafePass`는 모두 실무에서 사용하는 API입니다. 핵심은 **렌더패스의 목적에 맞게 선택하는 것**입니다.

| 상황 | 올바른 선택 |
|---|---|
| 단일 렌더 타겟, 픽셀 셰이더 기반 패스 | `AddRasterRenderPass` |
| Compute Shader dispatch | `AddComputePass` |
| `cmd.CopyTexture()`, `cmd.SetRenderTarget()` 직접 제어 | `AddUnsafePass` |
| 단일 패스 내 렌더 타겟 동적 전환 | `AddUnsafePass` |

WITHOUT skill은 단순 Blit 패스에 `AddUnsafePass`를 사용합니다. 이 패스는 `AddRasterRenderPass`로 구현 가능한 케이스이므로 RenderGraph 자동 최적화(패스 머징, 타일 최적화)를 불필요하게 포기합니다.

```csharp
// ❌ WITHOUT skill: 단순 Blit에 AddUnsafePass 사용 → RenderGraph 최적화 무력화
using (var builder = renderGraph.AddUnsafePass<PassData>("Radial Blur", out var passData))
{
    builder.SetRenderFunc(static (PassData data, UnsafeGraphContext ctx) =>
    {
        var cmd = CommandBufferHelpers.GetNativeCommandBuffer(ctx.cmd);
        cmd.Blit(data.source, data.source, data.material, 0); // ❌ source == dest
    });
}

// ✅ WITH skill: 단일 렌더 타겟 Blit → AddRasterRenderPass가 적합
using var builder = renderGraph.AddRasterRenderPass<PassData>("Radial Blur", out var passData);
builder.UseTexture(passData.source, AccessFlags.Read);
builder.SetRenderAttachment(resourceData.activeColorTexture, 0, AccessFlags.WriteAll);
builder.SetRenderFunc(static (PassData data, RasterGraphContext ctx) =>
{
    Blitter.BlitTexture(ctx.cmd, data.source, new Vector4(1f, 1f, 0f, 0f), data.material, 0);
});
```

---

### 검증 2 — 모바일 성능 최적화

**half 정밀도 + AccessFlags**

```hlsl
// ❌ WITHOUT skill
float4 color = float4(0, 0, 0, 0); // float: 모바일 레지스터 2배 소비
for (int i = 0; i < _SampleCount; i++) { ... }

// ✅ WITH skill
half4 color = (half4)0; // half: 모바일 ALU 처리량 ~2배
UNITY_LOOP  // [loop] 매핑: 런타임 변수 반복 → 코드 팽창 방지
for (int i = 0; i < sampleCount; i++) { ... }
```

```csharp
// ❌ WITHOUT skill: 렌더 타겟 미선언 → 타일 GPU가 이전 내용 불필요하게 로드
builder.UseTexture(passData.source, AccessFlags.Read);

// ✅ WITH skill: WriteAll → DontCare loadOp → 타일 메모리 초기화 비용 제거
builder.SetRenderAttachment(resourceData.activeColorTexture, 0, AccessFlags.WriteAll);
```

**흐름 제어 Attribute — 상황별 선택**

`UNITY_LOOP`(= `[loop]`) 하나만이 정답이 아닙니다. 반복 횟수와 조건 특성에 따라 올바른 attribute가 다릅니다.

| 상황 | 반복문 | 조건문 |
|---|---|---|
| 런타임 변수 반복 / 반복 횟수 많음 | `[loop]` (UNITY_LOOP) | — |
| 컴파일 상수 반복 / 횟수 적음 (≤ 8) | `[unroll]` | — |
| 조건값이 draw call 전체에서 동일 (uniform) | — | `[branch]` (UNITY_BRANCH) |
| 조건값이 픽셀마다 다름 (텍스처 샘플 결과 등) | — | `[flatten]` (UNITY_FLATTEN) |
| 조건 블록에 framebuffer fetch 포함 | — | `[branch]` 필수 |

```hlsl
// ✅ 런타임 변수 반복 → [loop], 내부에서 LOD 명시 필수
UNITY_LOOP
for (int i = 0; i < (int)_SampleCount; i++)
    color += SAMPLE_TEXTURE2D_LOD(_Tex, sampler_Tex, uv, 0);

// ✅ uniform 조건 → [branch]: false 경로 완전 스킵
UNITY_BRANCH
if (_FeatureEnabled > 0.5)
    color = ExpensiveEffect(color);

// ✅ 픽셀마다 다른 조건 → [flatten]: wave 분기 오버헤드 방지
UNITY_FLATTEN
if (roughness < _Threshold)
    color = BlurSample(uv);
```

---

### 검증 3 — Volume System 통합

WITHOUT skill은 `[Serializable]` 설정 클래스만 사용합니다. 이 경우 씬 구역별 파라미터 블렌딩, 카메라 오버라이드, 런타임 제어가 모두 불가능합니다.

```csharp
// ✅ WITH skill: VolumeComponent 완전 통합
[Serializable, VolumeComponentMenu("Post-processing/Radial Blur")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
public sealed class RadialBlurComponent : VolumeComponent, IPostProcessComponent
{
    public ClampedFloatParameter intensity   = new ClampedFloatParameter(0f, 0f, 1f);
    public Vector2Parameter      center      = new Vector2Parameter(new Vector2(0.5f, 0.5f));
    public ClampedIntParameter   sampleCount = new ClampedIntParameter(8, 4, 32);

    // intensity == 0 이면 패스를 GPU에 등록하지 않음
    public bool IsActive() => intensity.value > 0f;
}
```

| 기능 | WITH skill | WITHOUT skill |
|---|:---:|:---:|
| Volume Profile 편집 | ✅ | ❌ |
| 씬별 파라미터 블렌딩 | ✅ | ❌ |
| intensity = 0 시 패스 생략 | ✅ | ❌ (항상 실행) |

---

### 검증 4 — CBUFFER 타입 안전성

`int` 타입을 CBUFFER에 직접 선언하면 DX11 에디터에서는 정상 동작하지만, Metal/Vulkan 빌드에서 비트 해석 불일치로 이펙트가 오작동합니다.

```hlsl
// ❌ WITHOUT skill: CBUFFER 없음 + int 선언 (DX11만 안전)
int _SampleCount;

// ✅ WITH skill: CBUFFER_START + float 선언 후 셰이더 내부에서 캐스팅
CBUFFER_START(UnityPerMaterial)
    float _RadialBlurSampleCount; // int 의미이지만 float으로 선언
CBUFFER_END

int sampleCount = max(1, (int)_RadialBlurSampleCount); // 셰이더 내부 캐스팅
```

---

### 검증 5 — Blitter API 정합성

가장 발견하기 어려운 잠재 버그입니다. WITHOUT skill은 현재 동작하지만, `cmd.Blit` → `Blitter.BlitTexture`로 마이그레이션하는 순간 즉시 파손됩니다.

```
시나리오: "더 좋은 API"로 교체를 시도할 때

cmd.Blit(...)  →  Blitter.BlitTexture(...)  (변경)

결과:
  - 셰이더는 여전히 _MainTex 선언 유지
  - Blitter는 "_BlitTexture"에 소스 바인딩
  → _MainTex = 기본 흰 텍스처 = 화면 전체 하얗게 됨
```

```hlsl
// ❌ WITHOUT skill: _MainTex (현재는 동작, 마이그레이션 시 파손)
TEXTURE2D(_MainTex);
color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, sampleUV);

// ✅ WITH skill: _BlitTexture (Blitter API와 정확히 일치)
#include "Packages/com.unity.render-pipelines.core/Runtime/Utilities/Blit.hlsl"
color += (half4)SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_LinearClamp, sampleUV);
```

---



---

## 구현 사례: Screen Space Reflection

> **환경:** Unity 6000.3.10f1 / URP 17.3.0 / Android Vulkan 1.1+  
> **목표:** 모바일 Mid GPU 기준 1.5ms 이내로 동작하는 커스텀 SSR RendererFeature

URP 17에는 내장 SSR이 없습니다. 이 스킬을 활용해 RenderGraph 기반의 커스텀 SSR을 처음부터 구현했습니다.

<img width="1229" height="671" alt="image" src="https://github.com/user-attachments/assets/1d7ee61d-58eb-4e87-9de3-2074ad4d9699" />


### 아키텍처

```
RenderPassEvent.AfterRenderingOpaques
  ├── Pass 1: SSRRayMarchPass       — Linear ray march, half-resolution
  ├── Pass 2: SSRResolvePass        — Roughness 기반 bilateral blur
  └── Pass 3: SSRCompositePass      — Fresnel 가중치 합성
```

### Vulkan 1.1 모바일 호환 설계 판단

Android Vulkan 1.1 이상을 타겟으로 했기 때문에 다음 제약 조건을 설계 단계부터 반영했습니다.

**Compute Shader 미사용**  
Vulkan 1.1 기준으로 모든 기기에서 Compute 지원이 보장되지 않습니다. SSR Ray March를 Fragment Shader 기반으로 구현해 호환성을 확보했습니다.

**Hi-Z Mip Chain 제외**  
Hi-Z 가속 ray march는 별도 Hi-Z 맵 생성 비용이 발생하고, Mid-tier 모바일 GPU에서는 오히려 전체 비용이 증가합니다. Linear step ray march로 대체해 예측 가능한 성능을 확보했습니다.

**Temporal Accumulation 제외**  
Temporal은 Motion Vector 버퍼를 추가로 요구합니다. 모바일 메모리 대역폭 절약을 위해 제외하고, 대신 Bilateral Blur로 노이즈를 처리했습니다.

**Normal 재구성 함수 미사용**  
URP 17의 `cameraNormalsTexture`는 World Space Normal을 `R8G8B8A8_SNorm`으로 직접 저장합니다. 별도 재구성 함수 없이 직접 샘플링해 연산 비용을 줄였습니다.

### 도입한 최적화 기법

**ConfigureInput 자동 버퍼 요청**  
스킬의 `ConfigureInput` 패턴 가이드에 따라 URP Renderer Data 수동 설정 없이 Depth/Normal 버퍼를 자동 요청했습니다.

```csharp
// RendererFeature가 URP에 버퍼를 직접 요청 → DepthNormals Prepass 자동 활성화
m_OrchestratorPass.ConfigureInput(
    ScriptableRenderPassInput.Depth | ScriptableRenderPassInput.Normal
);
```

**Half-resolution Ray March**  
Ray March 패스를 화면 해상도의 50%로 실행하고, Resolve 패스에서 full-resolution으로 업스케일합니다. 픽셀 처리량이 4분의 1로 줄어 가장 비용이 큰 구간의 GPU 시간을 절약합니다.

**Interleaved Sampling**  
2×2 체커보드 패턴으로 프레임당 전체 픽셀의 1/4만 Ray March를 수행합니다. Resolve 패스의 Bilateral Blur가 빈 픽셀을 채웁니다.

**`activeColorTexture` 반사 색상 소스**  
Ray March 패스는 `activeColorTexture`를 읽기 전용(`AccessFlags.Read`)으로 참조하여 반사 색상을 샘플링하고, 결과는 별도의 half-res `ssrRawRT`에 씁니다. 이후 Composite 패스에서 `ssrResolvedRT`를 읽어 `activeColorTexture`에 Fresnel 블렌딩합니다. 각 패스가 서로 다른 버퍼를 읽고 쓰므로 read-write 충돌이 없으며, 별도 CopyColor 패스 없이 현재 화면 버퍼를 소스로 활용합니다.

**플랫폼 분기 처리**  
`UNITY_REVERSED_Z`(Vulkan/Metal depth 방향)와 `UNITY_UV_STARTS_AT_TOP`(UV 원점) 분기를 모든 셰이더에 적용해 DX11/Vulkan/Metal에서 동일한 결과를 보장합니다.

### 성능 목표

| GPU 티어 | 대표 GPU | SSR 목표 | 설정 |
|---|---|---|---|
| High | Adreno 750, Mali-G715 | < 2ms | 50% res, 32 steps |
| Mid | Adreno 640, Mali-G77 | < 1.5ms | 50% res, 24 steps |
| Low | Adreno 612, Mali-G57 | N/A | SSR 비활성, Probe Fallback |


---

## 스킬 ROI

스킬 없이 구현할 때 발생하는 예상 추가 비용입니다.

| 발생 원인 | 예상 디버깅 비용 |
|---|---|
| `_MainTex` vs `_BlitTexture` 불일치 버그 | 2~4시간 |
| `int` CBUFFER 모바일 오작동 (실기기 필요) | 4~8시간 |
| Volume System 미통합 후 재아키텍처 | 1~2일 |
| 모바일 성능 누락 후 프로파일링/수정 | 0.5~1일 |
| **합계** | **약 2~4일** |

이 함정들은 모두 에디터(DX11)에서는 정상처럼 보입니다. 실기기 빌드 또는 API 업그레이드 시점에야 증상이 나타납니다.

---

## 라이선스

MIT License © [CatDarkGame](https://github.com/CatDarkGame)

---

<a name="english"></a>

## Introduction

`unity-urp-dev` is a Claude Code skill that guides correct code generation when developing RenderGraph-based RendererFeatures for Unity URP.

The skill has two core functions.

**1. Advanced Rendering Reference**  
The `references/` folder documents advanced techniques needed for real-world implementation: RenderGraph API patterns, Job System / Burst compiler, Compute Shaders, and unsafe zero-copy memory transfers. Claude Code reads these references directly and writes code using validated patterns.

**2. URP Version-Aware Code Generation**  
Before starting any task, the skill automatically detects the project's URP version. It then references the official Unity Docs and URP GitHub source for that specific version, preventing errors caused by API differences between versions.

<img width="1229" height="671" alt="image" src="https://github.com/user-attachments/assets/d5da7338-b14d-404c-aa38-212e885ce747" />


### Coverage

| Keyword | Content |
|---|---|
| `RenderGraph` | `AddRasterRenderPass`, `AddUnsafePass`, `AddComputePass` patterns |
| `RendererFeature` | Full `ScriptableRendererFeature` structure and Volume integration |
| `PostProcessing` | Bloom, DoF, Motion Blur, SSAO, TAA, custom effects |
| `HLSL / ShaderLibrary` | `Blit.hlsl`, math functions, color space conversion, mobile precision |
| `Compute Shader` | Compute Pass, AsyncGPUReadback, GPU Culling |
| `Unity 6.0` | GPU Resident Drawer, RenderGraph Viewer debugging |

---

## Installation

### Manual Installation

```bash
# 1. Navigate to the Claude Code skills directory
cd ~/.claude/skills

# 2. Clone the repository
git clone https://github.com/CatDarkGame/claude-skill-unity-urp unity-urp-dev
```

Once installed, the skill activates automatically during URP-related work in Claude Code.

### Activation Triggers

The skill loads automatically when URP RenderGraph and RendererFeature development keywords appear in the conversation. Claude Code detects relevant keywords and matches them against the `SKILL.md` description to load the skill context.

`URP` · `RenderGraph` · `RendererFeature` · `ScriptableRenderPass` · `PostProcess` · `HLSL` · `SSR` · `Bloom` · `DoF` · `TAA` · `Compute Shader` · `Burst` · `Job System` · and more

---

## Skill Structure

```
unity-urp-dev/
├── SKILL.md                              # Skill entry point (version detection → reference routing)
└── references/
    ├── 01_URP_Core_Package_Guide.md      # RenderGraph core pass structure
    ├── 02_RenderPipelineCore_Guide.md    # Volume System, VolumeComponent
    ├── 03_PostProcessing_Effects_Guide.md # Bloom, DoF, TAA, SSAO implementation
    ├── 04_ShaderLibrary_Guide.md         # HLSL, ShaderLibrary, sampling patterns
    ├── 05_Mathematics_Collections_Guide.md # Unity.Mathematics, Burst, Job System
    ├── 06_Unity60_NewFeatures_Guide.md   # Unity 6.0 new features
    ├── 07_Advanced_Memory_Management_Guide.md # Constant Buffer, GPU memory
    └── 08_Compute_Shader_Integration_Guide.md # Compute Pass, GPU Culling
```

The skill's first step is automatic detection of the project's URP version. Since APIs differ between versions, code generation never starts without version verification.

---

## Validation: With vs Without Skill

> **Test environment:** Unity 6000.3.10f1 / URP 17.3.0  
> **Target feature:** Radial Blur post-processing effect  
> **Method:** Independent implementation with and without the skill, using identical feature requirements

<img width="1125" height="634" alt="image" src="https://github.com/user-attachments/assets/58fac3f7-3d01-4f48-bfc4-952c525aee59" />


### Summary

| # | Validation Item | WITH skill | WITHOUT skill | Real-world Impact |
|---|---|:---:|:---:|---|
| 1 | URP 17 RenderGraph compliance | ✅ | ❌ | RenderGraph Validator warnings |
| 2 | Mobile performance optimization | ✅ | ❌ | ~20-35% higher GPU cost |
| 3 | Volume System integration | ✅ | ❌ | No per-scene parameter blending |
| 4 | CBUFFER type safety | ✅ | ❌ | Potential bugs on Metal/Vulkan |
| 5 | Blitter API correctness | ✅ | ❌ | Full white screen on API migration |

---

### Validation 1 — RenderGraph API Selection

Both `AddRasterRenderPass` and `AddUnsafePass` are valid in production. The key is **choosing the one that matches the render pass's purpose**.

| Situation | Correct Choice |
|---|---|
| Single render target, pixel shader-based pass | `AddRasterRenderPass` |
| Compute Shader dispatch | `AddComputePass` |
| Direct `cmd.CopyTexture()` / `cmd.SetRenderTarget()` control | `AddUnsafePass` |
| Dynamic render target switching within a single pass | `AddUnsafePass` |

WITHOUT skill uses `AddUnsafePass` for a simple Blit pass — a case that `AddRasterRenderPass` handles correctly. This unnecessarily sacrifices RenderGraph automatic optimizations (pass merging, tile optimization).

```csharp
// ❌ WITHOUT skill: AddUnsafePass for a simple Blit → disables RenderGraph optimization
using (var builder = renderGraph.AddUnsafePass<PassData>("Radial Blur", out var passData))
{
    builder.SetRenderFunc(static (PassData data, UnsafeGraphContext ctx) =>
    {
        var cmd = CommandBufferHelpers.GetNativeCommandBuffer(ctx.cmd);
        cmd.Blit(data.source, data.source, data.material, 0); // ❌ source == dest
    });
}

// ✅ WITH skill: single render target Blit → AddRasterRenderPass is the right choice
using var builder = renderGraph.AddRasterRenderPass<PassData>("Radial Blur", out var passData);
builder.UseTexture(passData.source, AccessFlags.Read);
builder.SetRenderAttachment(resourceData.activeColorTexture, 0, AccessFlags.WriteAll);
builder.SetRenderFunc(static (PassData data, RasterGraphContext ctx) =>
{
    Blitter.BlitTexture(ctx.cmd, data.source, new Vector4(1f, 1f, 0f, 0f), data.material, 0);
});
```

---

### Validation 2 — Mobile Performance Optimization

**half precision + AccessFlags**

```hlsl
// ❌ WITHOUT skill
float4 color = float4(0, 0, 0, 0); // float: 2x register usage on mobile
for (int i = 0; i < _SampleCount; i++) { ... }

// ✅ WITH skill
half4 color = (half4)0; // half: ~2x ALU throughput on mobile
UNITY_LOOP  // [loop] mapping: runtime variable iteration → prevents code bloat
for (int i = 0; i < sampleCount; i++) { ... }
```

```csharp
// ❌ WITHOUT skill: no render target declaration → tile GPU unnecessarily loads previous content
builder.UseTexture(passData.source, AccessFlags.Read);

// ✅ WITH skill: WriteAll → DontCare loadOp → eliminates tile memory initialization cost
builder.SetRenderAttachment(resourceData.activeColorTexture, 0, AccessFlags.WriteAll);
```

**Flow Control Attributes — Choosing by Situation**

`UNITY_LOOP` (= `[loop]`) is not the universal answer. The correct attribute depends on iteration count and condition characteristics.

| Situation | Loop | Condition |
|---|---|---|
| Runtime variable iteration / many iterations | `[loop]` (UNITY_LOOP) | — |
| Compile-time constant / few iterations (≤ 8) | `[unroll]` | — |
| Condition uniform across entire draw call | — | `[branch]` (UNITY_BRANCH) |
| Condition varies per pixel (texture sample result, etc.) | — | `[flatten]` (UNITY_FLATTEN) |
| Condition block contains framebuffer fetch | — | `[branch]` required |

```hlsl
// ✅ Runtime variable iteration → [loop], explicit LOD inside loop required
UNITY_LOOP
for (int i = 0; i < (int)_SampleCount; i++)
    color += SAMPLE_TEXTURE2D_LOD(_Tex, sampler_Tex, uv, 0);

// ✅ Uniform condition → [branch]: false path completely skipped
UNITY_BRANCH
if (_FeatureEnabled > 0.5)
    color = ExpensiveEffect(color);

// ✅ Per-pixel divergent condition → [flatten]: prevents wave divergence overhead
UNITY_FLATTEN
if (roughness < _Threshold)
    color = BlurSample(uv);
```

---

### Validation 3 — Volume System Integration

WITHOUT skill uses only a `[Serializable]` settings class. This makes per-zone parameter blending, camera overrides, and runtime control impossible.

```csharp
// ✅ WITH skill: full VolumeComponent integration
[Serializable, VolumeComponentMenu("Post-processing/Radial Blur")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
public sealed class RadialBlurComponent : VolumeComponent, IPostProcessComponent
{
    public ClampedFloatParameter intensity   = new ClampedFloatParameter(0f, 0f, 1f);
    public Vector2Parameter      center      = new Vector2Parameter(new Vector2(0.5f, 0.5f));
    public ClampedIntParameter   sampleCount = new ClampedIntParameter(8, 4, 32);

    // Skip GPU registration when intensity == 0
    public bool IsActive() => intensity.value > 0f;
}
```

| Feature | WITH skill | WITHOUT skill |
|---|:---:|:---:|
| Volume Profile editing | ✅ | ❌ |
| Per-scene parameter blending | ✅ | ❌ |
| Pass skipped when intensity = 0 | ✅ | ❌ (always runs) |

---

### Validation 4 — CBUFFER Type Safety

Declaring `int` directly in a CBUFFER works in the DX11 editor but causes bit-interpretation mismatches in Metal/Vulkan builds, breaking the effect.

```hlsl
// ❌ WITHOUT skill: no CBUFFER + int declaration (safe only on DX11)
int _SampleCount;

// ✅ WITH skill: CBUFFER_START + float declaration, cast inside shader
CBUFFER_START(UnityPerMaterial)
    float _RadialBlurSampleCount; // semantically int, declared as float
CBUFFER_END

int sampleCount = max(1, (int)_RadialBlurSampleCount); // cast inside shader
```

---

### Validation 5 — Blitter API Correctness

The hardest bug to find. WITHOUT skill works now, but breaks the moment `cmd.Blit` is migrated to `Blitter.BlitTexture`.

```
Scenario: attempting to upgrade to the "better API"

cmd.Blit(...)  →  Blitter.BlitTexture(...)  (changed)

Result:
  - Shader still declares _MainTex
  - Blitter binds the source to "_BlitTexture"
  → _MainTex = default white texture = entire screen turns white
```

```hlsl
// ❌ WITHOUT skill: _MainTex (works now, breaks on migration)
TEXTURE2D(_MainTex);
color += SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, sampleUV);

// ✅ WITH skill: _BlitTexture (matches Blitter API exactly)
#include "Packages/com.unity.render-pipelines.core/Runtime/Utilities/Blit.hlsl"
color += (half4)SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_LinearClamp, sampleUV);
```

---



---

## Case Study: Screen Space Reflection

> **Environment:** Unity 6000.3.10f1 / URP 17.3.0 / Android Vulkan 1.1+  
> **Goal:** Custom SSR RendererFeature targeting < 1.5ms on mobile Mid-tier GPU

URP 17 has no built-in SSR. This skill was used to implement a RenderGraph-based custom SSR from scratch.

<img width="1229" height="671" alt="image" src="https://github.com/user-attachments/assets/1d7ee61d-58eb-4e87-9de3-2074ad4d9699" />


### Architecture

```
RenderPassEvent.AfterRenderingOpaques
  ├── Pass 1: SSRRayMarchPass       — Linear ray march, half-resolution
  ├── Pass 2: SSRResolvePass        — Roughness-based bilateral blur
  └── Pass 3: SSRCompositePass      — Fresnel-weighted compositing
```

### Vulkan 1.1 Mobile Compatibility Design Decisions

Targeting Android Vulkan 1.1+, the following constraints were baked into the architecture from the start.

**No Compute Shaders**  
Compute support is not guaranteed across all devices at Vulkan 1.1. SSR ray marching was implemented in Fragment Shader to ensure compatibility.

**No Hi-Z Mip Chain**  
Hi-Z accelerated ray marching incurs a separate Hi-Z map generation cost. On mid-tier mobile GPUs this increases total cost rather than reducing it. Linear step ray marching was used instead for predictable performance.

**No Temporal Accumulation**  
Temporal requires an additional Motion Vector buffer. Excluded to save mobile memory bandwidth; bilateral blur handles noise reduction instead.

**No Normal Reconstruction**  
URP 17's `cameraNormalsTexture` stores World Space Normals directly as `R8G8B8A8_SNorm`. Direct sampling eliminates reconstruction pass overhead.

### Optimizations Applied

**ConfigureInput for Automatic Buffer Requests**  
Following the skill's `ConfigureInput` pattern guide, Depth/Normal buffers are requested automatically without manual URP Renderer Data configuration.

```csharp
// RendererFeature requests buffers directly from URP → auto-enables DepthNormals Prepass
m_OrchestratorPass.ConfigureInput(
    ScriptableRenderPassInput.Depth | ScriptableRenderPassInput.Normal
);
```

**Half-Resolution Ray March**  
The ray march pass runs at 50% screen resolution and upscales to full resolution in the Resolve pass. Pixel throughput is reduced to one quarter, saving GPU time in the most expensive stage.

**Interleaved Sampling**  
A 2×2 checkerboard pattern processes only 1/4 of all pixels per frame. The Resolve pass's bilateral blur fills in the remaining pixels.

**`activeColorTexture` as Reflection Color Source**  
The ray march pass references `activeColorTexture` read-only (`AccessFlags.Read`) for reflection color sampling and writes results to a separate half-res `ssrRawRT`. The Composite pass then reads `ssrResolvedRT` and blends it into `activeColorTexture` via Fresnel weighting. Each pass reads and writes different buffers, eliminating read-write conflicts — no separate CopyColor pass needed.

**Platform Branching**  
`UNITY_REVERSED_Z` (Vulkan/Metal depth direction) and `UNITY_UV_STARTS_AT_TOP` (UV origin) branches are applied in all shaders, ensuring identical results across DX11/Vulkan/Metal.

### Performance Targets

| GPU Tier | Representative GPU | SSR Target | Settings |
|---|---|---|---|
| High | Adreno 750, Mali-G715 | < 2ms | 50% res, 32 steps |
| Mid | Adreno 640, Mali-G77 | < 1.5ms | 50% res, 24 steps |
| Low | Adreno 612, Mali-G57 | N/A | SSR disabled, Probe Fallback |


---

## Skill ROI

Estimated additional cost of implementing without this skill.

| Root Cause | Estimated Debug Cost |
|---|---|
| `_MainTex` vs `_BlitTexture` mismatch bug | 2–4 hours |
| `int` CBUFFER mobile malfunction (requires device build) | 4–8 hours |
| Volume System retrofit after initial architecture | 1–2 days |
| Mobile performance regression: profiling + fixes | 0.5–1 day |
| **Total** | **~2–4 days** |

Every one of these traps looks fine in the editor (DX11). Symptoms only appear on a device build or when upgrading the API.

---

## License

MIT License © [CatDarkGame](https://github.com/CatDarkGame)

---

<div align="center">

Made with ❤️ for Unity developers

</div>
