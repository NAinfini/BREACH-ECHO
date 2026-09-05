# Unity 6.0 URP 코어 패키지 RenderGraph 개발 가이드

## 개요

Unity 6.0의 URP(Universal Render Pipeline) 코어 패키지(`com.unity.render-pipelines.universal`)에서 RenderGraph API를 사용한 커스텀 포스트프로세싱 효과 개발을 위한 완전한 가이드입니다.

## 목차

1. [RenderGraph API 핵심 패턴](#rendergraph-api-핵심-패턴)
2. [ScriptableRenderPass 구현](#scriptablerenderpass-구현)
3. [Built-in Post-processing 분석](#built-in-post-processing-분석)
4. [텍스처 관리 전략](#텍스처-관리-전략)
5. [Volume System 통합](#volume-system-통합)
6. [필수 네임스페이스](#필수-네임스페이스)
7. [실제 구현 예제](#실제-구현-예제)
8. [성능 최적화](#성능-최적화)
9. [문제해결 가이드](#문제해결-가이드)

---

## RenderGraph API 핵심 패턴

### PassData 클래스 정의 규칙

**❌ 잘못된 방법 (struct 사용)**:
```csharp
// 이것은 작동하지 않습니다!
private struct MyPassData  // struct는 reference type이 아니므로 오류 발생
{
    public TextureHandle sourceTexture;
}
```

**✅ 올바른 방법 (class 사용)**:
```csharp
private class MyPassData
{
    // Setup parameters
    internal EffectParameters parameters;
    internal bool enableQuality;
    
    // Input textures
    internal TextureHandle sourceTexture;
    internal TextureHandle depthTexture;
    
    // Materials
    internal Material material;
    
    // Intermediate textures
    internal TextureHandle tempTexture1;
    internal TextureHandle tempTexture2;
    
    // Output
    internal TextureHandle destination;
}
```

**핵심 규칙**:
- **class**로 정의 (struct 사용 시 컴파일 오류)
- 모든 필드는 **internal** 접근자 사용
- 논리적 그룹별로 섹션 분리 (Setup → Input → Material → Temp → Output)

### AddRasterRenderPass vs AddUnsafePass vs AddComputePass 선택 기준

#### 세 가지 Pass API 비교표

| 항목 | `AddRasterRenderPass` | `AddUnsafePass` | `AddComputePass` |
|------|----------------------|-----------------|------------------|
| **컨텍스트 타입** | `RasterGraphContext` | `UnsafeGraphContext` | `ComputeGraphContext` |
| **렌더 타겟 설정** | `SetRenderAttachment` (RecordRenderGraph에서 선언) | `cmd.SetRenderTarget` (SetRenderFunc 내부에서 직접) | 해당 없음 (렌더 타겟 없음) |
| **CommandBuffer 접근** | `RasterCommandBuffer` (제한된 API) | `UnsafeCommandBuffer` (전체 CommandBuffer API) | `ComputeCommandBuffer` |
| **RenderGraph 자동 최적화** | 최대 (패스 머징, 타일 최적화 가능) | 없음 (모든 native render pass 직렬화됨) | 있음 (compute 범위 내) |
| **의존성 자동 추적** | 있음 (`UseTexture`로 선언 → 자동 검증) | 제한적 (선언은 하지만 내부 동작은 사용자 책임) | 있음 |
| **`SetRenderTarget` 사용** | 불가 | 가능 (`context.cmd.SetRenderTarget`) | 해당 없음 |
| **`CopyTexture` 등 고급 CB API** | 불가 | 가능 (`CommandBufferHelpers.GetNativeCommandBuffer`) | 불가 |
| **모바일 타일 GPU 최적화** | 가능 (on-tile memory, framebuffer fetch 활용) | 불가 (타일 경계 강제 분리) | 해당 없음 |
| **사용 난이도** | 다소 엄격 (명시적 attachment 선언 필요) | 유연 | 중간 |
| **권장 여부** | 기본 선택 (장기적으로 최적화 이득) | 필요한 경우에만 사용 | CS dispatch 전용 |

---

#### 실무 판단 체크리스트

```
패스 목적을 먼저 파악한다:

1. Compute Shader를 dispatch하는 패스인가?
   → YES: AddComputePass 사용. 끝.

2. 픽셀 셰이더(Blit, DrawRenderer, DrawProcedural)로 렌더 타겟에 쓰는 패스인가?
   → YES: 아래 3번으로 진행.

3. 다음 중 하나라도 해당하는가?
   - cmd.SetRenderTarget()을 직접 호출해야 한다
   - cmd.CopyTexture() / cmd.Blit() 등 CommandBuffer 직접 API가 필요하다
   - 패스 내부에서 렌더 타겟을 동적으로 전환해야 한다 (멀티패스 구조)
   - 기존 CommandBuffer 기반 코드를 RenderGraph로 점진적으로 이식 중이다
   → YES: AddUnsafePass 사용.
   → NO: AddRasterRenderPass 사용 (권장).
```

---

#### AddRasterRenderPass (기본 선택)

**적합한 경우:**
- 단일 렌더 타겟(또는 MRT)으로의 Blit/Draw 작업
- `SetRenderAttachment`로 attachment를 RecordRenderGraph 단계에서 선언 가능한 패스
- 모바일(TBDR GPU) 최적화가 중요한 프로젝트
- 인접한 패스와 자동 패스 머징(merge) 혜택을 받으려는 경우

**제약:**
- `SetRenderTarget` 직접 호출 불가 (RecordRenderGraph에서 `SetRenderAttachment`로 대신)
- 패스 실행 중 렌더 타겟 동적 전환 불가

```csharp
using (var builder = renderGraph.AddRasterRenderPass<StopNaNsPassData>("Stop NaNs", out var passData,
               ProfilingSampler.Get(URPProfileId.RG_StopNaNs)))
{
    // 텍스처 의존성을 RecordRenderGraph 단계에서 명시적으로 선언
    passData.sourceTexture = activeCameraColor;
    passData.material = stopNaNMaterial;
    
    builder.UseTexture(activeCameraColor, AccessFlags.Read);
    builder.SetRenderAttachment(stopNaNTarget, 0, AccessFlags.Write);  // cmd.SetRenderTarget 대신
    
    // RasterGraphContext: RasterCommandBuffer 사용
    builder.SetRenderFunc(static (StopNaNsPassData data, RasterGraphContext context) =>
    {
        var cmd = context.cmd;  // RasterCommandBuffer — SetRenderTarget 호출 불가
        RTHandle sourceHandle = data.sourceTexture;
        Vector2 viewportScale = sourceHandle.useScaling ? 
            new Vector2(sourceHandle.rtHandleProperties.rtHandleScale.x, 
                       sourceHandle.rtHandleProperties.rtHandleScale.y) : 
            Vector2.one;
        Blitter.BlitTexture(cmd, sourceHandle, viewportScale, data.material, 0);
    });
}
```

---

#### AddUnsafePass (필요한 경우에만)

**적합한 경우:**
- `cmd.SetRenderTarget()`을 직접 제어해야 하는 경우
- `cmd.CopyTexture()`, `cmd.Blit()` 등 전체 CommandBuffer API가 필요한 경우
- 하나의 패스 안에서 여러 렌더 타겟을 순차적으로 전환하는 멀티패스 구조 (Bloom, DoF 등)
- 기존 CommandBuffer 기반 패스를 RenderGraph로 점진적으로 마이그레이션하는 경우

**Trade-off:**
- URP가 패스 내부 동작을 알 수 없으므로 자동 최적화(패스 머징, 타일 메모리 활용) 불가
- 모든 native render pass가 직렬화되어 GPU 대역폭 낭비 가능
- 의존성 자동 검증이 약해 누락된 `UseTexture` 선언으로 인한 버그 위험

```csharp
using (var builder = renderGraph.AddUnsafePass<DoFBokehPassData>("Depth of Field - Bokeh", out var passData))
{
    // 여러 중간 텍스처를 ReadWrite로 선언 (의존성 추적용 — 실제 binding은 SetRenderTarget으로)
    builder.UseTexture(fullCoCTexture, AccessFlags.ReadWrite);
    builder.UseTexture(pingTexture, AccessFlags.ReadWrite);
    builder.UseTexture(pongTexture, AccessFlags.ReadWrite);
    builder.UseTexture(destination, AccessFlags.Write);
    
    // UnsafeGraphContext: 전체 CommandBuffer API 접근 가능
    builder.SetRenderFunc(static (DoFBokehPassData data, UnsafeGraphContext context) =>
    {
        // SetRenderTarget 직접 제어 가능
        context.cmd.SetRenderTarget(data.fullCoCTexture);
        
        // 전체 CommandBuffer API가 필요한 경우 native buffer 획득
        CommandBuffer cmd = CommandBufferHelpers.GetNativeCommandBuffer(context.cmd);
        ExecuteComplexBokehBlur(data, cmd);
    });
}
```

**중요**: `AddUnsafePass`에서는 `SetRenderAttachment`를 RecordRenderGraph 단계에서 호출하면 안 된다. 대신 `SetRenderFunc` 내부에서 `context.cmd.SetRenderTarget()`을 사용한다.

---

#### AddComputePass (Compute Shader 전용)

**적합한 경우:**
- `ComputeShader.Dispatch`를 통한 GPU 연산
- 렌더 타겟 없이 Buffer/Texture를 읽고 쓰는 패스

```csharp
using (var builder = renderGraph.AddComputePass<ComputePassData>("My Compute Pass", out var passData))
{
    passData.computeShader = myComputeShader;
    passData.output = renderGraph.ImportBuffer(outputBuffer);
    
    builder.UseBuffer(passData.output, AccessFlags.Write);
    
    // ComputeGraphContext: DispatchCompute API 사용
    builder.SetRenderFunc(static (ComputePassData data, ComputeGraphContext context) =>
    {
        context.cmd.SetComputeBufferParam(data.computeShader,
            data.computeShader.FindKernel("Main"), "outputData", data.output);
        context.cmd.DispatchCompute(data.computeShader,
            data.computeShader.FindKernel("Main"), 1, 1, 1);
    });
}
```

---

### TextureHandle 생성 및 사용법

#### 텍스처 생성 (권장 방법)
```csharp
// URP 표준 임시 텍스처 Descriptor 구성
// PostProcessPass.GetCompatibleDescriptor는 internal API이므로 직접 구성한다
var desc = cameraDescriptor;
desc.width           = width;
desc.height          = height;
desc.graphicsFormat  = GraphicsFormat.B10G11R11_UFloatPack32;
desc.depthBufferBits = 0;   // 포스트프로세스 텍스처는 depth buffer 불필요
desc.msaaSamples     = 1;   // MSAA 비활성화

TextureHandle myTexture = UniversalRenderer.CreateRenderGraphTexture(
    renderGraph, 
    desc, 
    "_MyTextureName", 
    clear: true,                    // 텍스처 클리어 여부
    FilterMode.Bilinear,           // 필터링 모드
    TextureWrapMode.Clamp          // 래핑 모드
);
```

#### AccessFlags 최적화 규칙

`SetRenderAttachment`에 `AccessFlags.Write` 또는 `AccessFlags.WriteAll`을 지정하면, RenderGraph는 해당 렌더 타겟의 이전 내용을 로드할 필요가 없음을 인식한다. 타일 기반 GPU(Mali, Adreno)에서는 이것이 loadOp.DontCare로 변환되어 타일 메모리 초기화 비용이 제거된다. 전체 화면을 덮어쓰는 포스트프로세스 패스에서 반드시 사용해야 한다.

- `AccessFlags.Write` — 렌더 타겟에 쓰되 이전 내용 로드 없음 → DontCare loadOp
- `AccessFlags.WriteAll` (`Write | Discard`) — 전체 픽셀 덮어씀을 명시. 의도를 가장 명확하게 표현

```csharp
// 성능별 AccessFlags 우선순위
builder.UseTexture(sourceTexture, AccessFlags.Read);        // 최고 성능
builder.UseTexture(tempTexture, AccessFlags.Write);         // 고성능
builder.UseTexture(inOutTexture, AccessFlags.ReadWrite);    // 낮은 성능 (필요한 경우에만)

// 렌더 어태치먼트 설정 — 포스트프로세스 전체 화면 덮어쓰기
builder.SetRenderAttachment(outputTexture, 0, AccessFlags.WriteAll);  // DontCare loadOp 유도 (권장)
builder.SetRenderAttachment(outputTexture, 0, AccessFlags.Write);     // 단일 타겟
builder.SetRenderAttachment(outputTexture, 0, AccessFlags.ReadWrite); // 읽기도 필요한 경우
```

---

## ScriptableRenderPass 구현

### 기본 구조

```csharp
public class CustomPostProcessPass : ScriptableRenderPass
{
    private Material m_Material;
    private CustomPostProcessSettings m_Settings;
    
    // ProfilingSampler는 성능 측정용 (선택사항)
    private static readonly ProfilingSampler s_ProfilingSampler = 
        new ProfilingSampler("Custom Post Process");
    
    public CustomPostProcessPass(Material material, CustomPostProcessSettings settings)
    {
        m_Material = material;
        m_Settings = settings;
        
        // 렌더링 이벤트 시점 설정
        renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }
    
    // RenderGraph 방식 구현 (Unity 6.0 권장)
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        // 프레임 데이터 추출
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        // 효과가 활성화되지 않은 경우 스킵
        if (!ShouldRender(cameraData))
            return;
            
        ExecuteCustomPostProcess(renderGraph, resourceData, cameraData);
    }
    
    private void ExecuteCustomPostProcess(RenderGraph renderGraph, 
                                        UniversalResourceData resourceData, 
                                        UniversalCameraData cameraData)
    {
        using (var builder = renderGraph.AddRasterRenderPass<CustomPostProcessData>(
            "Custom Post Process", out var passData, s_ProfilingSampler))
        {
            // PassData 설정
            passData.material = m_Material;
            passData.settings = m_Settings;
            passData.sourceTexture = resourceData.activeColorTexture;
            
            // 출력 텍스처 생성 (PostProcessPass.GetCompatibleDescriptor는 internal — 직접 구성)
            var outputDesc = cameraData.cameraTargetDescriptor;
            outputDesc.depthBufferBits = 0;
            outputDesc.msaaSamples    = 1;
            
            passData.destination = UniversalRenderer.CreateRenderGraphTexture(
                renderGraph, outputDesc, "_CustomPostProcessOutput", true);
            
            // 리소스 의존성
            builder.UseTexture(passData.sourceTexture, AccessFlags.Read);
            builder.SetRenderAttachment(passData.destination, 0, AccessFlags.Write);
            
            // 실행 함수
            builder.SetRenderFunc(static (CustomPostProcessData data, RasterGraphContext context) =>
            {
                ExecutePass(data, context);
            });
        }
    }
    
    private static void ExecutePass(CustomPostProcessData data, RasterGraphContext context)
    {
        var cmd = context.cmd;
        
        // 셰이더 프로퍼티 설정
        data.material.SetFloat("_Intensity", data.settings.intensity);
        data.material.SetVector("_Parameters", data.settings.parameters);
        
        // 블릿 실행
        RTHandle sourceHandle = data.sourceTexture;
        Vector2 viewportScale = sourceHandle.useScaling ? 
            new Vector2(sourceHandle.rtHandleProperties.rtHandleScale.x,
                       sourceHandle.rtHandleProperties.rtHandleScale.y) : 
            Vector2.one;
            
        Blitter.BlitTexture(cmd, sourceHandle, viewportScale, data.material, 0);
    }
    
    private bool ShouldRender(UniversalCameraData cameraData)
    {
        return cameraData.camera.cameraType == CameraType.Game && 
               m_Settings.IsActive();
    }
}

private class CustomPostProcessData
{
    internal Material material;
    internal CustomPostProcessSettings settings;
    internal TextureHandle sourceTexture;
    internal TextureHandle destination;
}
```

### 렌더링 이벤트 시점 선택

```csharp
public enum RenderPassEvent
{
    // 포스트프로세싱 관련 주요 시점들
    BeforeRenderingPostProcessing = 550,    // 포스트프로세싱 이전 (톤매핑 전)
    AfterRenderingPostProcessing = 600,     // 포스트프로세싱 이후 (톤매핑 후)
    AfterRendering = 1000,                  // 모든 렌더링 완료 후
    
    // 기타 유용한 시점들
    AfterRenderingOpaques = 300,           // 불투명 오브젝트 렌더링 후
    BeforeRenderingTransparents = 450,     // 투명 오브젝트 렌더링 전
    AfterRenderingTransparents = 500,      // 투명 오브젝트 렌더링 후
}

// 사용 예시
renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing; // 일반적인 포스트프로세싱
renderPassEvent = RenderPassEvent.BeforeRenderingPostProcessing; // 톤매핑 전 적용
```

---

## Built-in Post-processing 분석

### Bloom 효과 구조 분석

```csharp
public void RenderBloomTexture(RenderGraph renderGraph, in TextureHandle source, 
                             out TextureHandle destination, bool enableAlphaOutput)
{
    // 1. 파라미터 설정
    var scatter = Vector4.one * m_Bloom.scatter.value;
    var clamp = m_Bloom.clamp.value;
    var threshold = Mathf.GammaToLinearSpace(m_Bloom.threshold.value);
    var thresholdKnee = threshold * 0.5f;
    
    BloomMaterialParams bloomParams = new BloomMaterialParams();
    bloomParams.parameters = new Vector4(scatter.x, clamp, threshold, thresholdKnee);
    bloomParams.highQualityFiltering = m_Bloom.highQualityFiltering.value;
    
    // 2. 밉맵 피라미드 생성 준비
    int mipCount = Mathf.Clamp(m_Bloom.maxIterations.value, 1, k_MaxPyramidSize);
    var desc = m_Descriptor;                   // PostProcessPass.GetCompatibleDescriptor는 internal — 직접 구성
    desc.graphicsFormat  = m_DefaultHDRFormat;
    desc.depthBufferBits = 0;
    desc.msaaSamples     = 1;
    
    // 3. 다운샘플링 텍스처들 생성
    var mipDown = new TextureHandle[mipCount];
    var mipUp = new TextureHandle[mipCount];
    
    mipDown[0] = source;  // 첫 번째는 소스 텍스처
    
    int tw = desc.width;
    int th = desc.height;
    
    for (int i = 1; i < mipCount; i++)
    {
        tw = Mathf.Max(1, tw >> 1);
        th = Mathf.Max(1, th >> 1);
        desc.width = tw;
        desc.height = th;
        
        mipDown[i] = UniversalRenderer.CreateRenderGraphTexture(
            renderGraph, desc, $"_BloomMipDown{i}", false, FilterMode.Bilinear);
        mipUp[i] = UniversalRenderer.CreateRenderGraphTexture(
            renderGraph, desc, $"_BloomMipUp{i}", false, FilterMode.Bilinear);
    }
    
    // 4. 블룸 패스 실행 (다운샘플 → 업샘플)
    using (var builder = renderGraph.AddUnsafePass<BloomPassData>(
        "Bloom", out var passData, ProfilingSampler.Get(URPProfileId.Bloom)))
    {
        // 모든 밉맵 텍스처를 PassData에 등록
        for (int i = 0; i < mipCount; i++)
        {
            if (i > 0)
            {
                builder.UseTexture(mipDown[i], AccessFlags.ReadWrite);
                builder.UseTexture(mipUp[i], AccessFlags.ReadWrite);
            }
        }
        
        // PassData 설정
        passData.mipDown = mipDown;
        passData.mipUp = mipUp;
        passData.bloomParams = bloomParams;
        passData.mipCount = mipCount;
        
        builder.SetRenderFunc(static (BloomPassData data, UnsafeGraphContext context) =>
        {
            ExecuteBloomPasses(data, context);
        });
    }
    
    destination = mipUp[0];  // 최종 결과는 첫 번째 업샘플 텍스처
}
```

### Depth of Field 효과 분석

#### Gaussian DoF 구현
```csharp
public void RenderDoFGaussian(RenderGraph renderGraph, /* parameters */)
{
    // 1. CoC(Circle of Confusion) 파라미터 계산
    float farStart = m_DepthOfField.gaussianStart.value;
    float farEnd = Mathf.Max(farStart, m_DepthOfField.gaussianEnd.value);
    
    // 해상도에 따른 반지름 스케일링
    float maxRadius = m_DepthOfField.gaussianMaxRadius.value * (cameraData.cameraTargetDescriptor.width / 1080f);
    maxRadius = Mathf.Min(maxRadius, 2f);  // 최대값 제한
    
    var cocParams = new Vector3(farStart, farEnd, maxRadius);
    
    // 2. 5패스 구조
    // Pass 1: CoC 맵 생성
    // Pass 2: 다운샘플 + 프리필터
    // Pass 3: 수평 블러
    // Pass 4: 수직 블러 
    // Pass 5: 업샘플 + 합성
    
    using (var builder = renderGraph.AddUnsafePass<DoFGaussianPassData>(
        "Depth of Field - Gaussian", out var passData))
    {
        // 중간 텍스처들 생성
        passData.fullCoCTexture = CreateCoCSizeTexture(renderGraph);
        passData.pingTexture = CreateHalfResTexture(renderGraph);
        passData.pongTexture = CreateHalfResTexture(renderGraph);
        
        // 파라미터 설정
        passData.cocParams = cocParams;
        passData.downsample = 2;  // 성능을 위한 다운샘플링
        
        builder.SetRenderFunc(static (DoFGaussianPassData data, UnsafeGraphContext context) =>
        {
            ExecuteGaussianDoF(data, context);
        });
    }
}
```

#### Bokeh DoF 구현 (물리 기반)
```csharp
public void RenderDoFBokeh(RenderGraph renderGraph, /* parameters */)
{
    // 1. 물리적 카메라 파라미터
    float F = m_DepthOfField.focalLength.value / 1000f;        // 초점거리(m)
    float A = m_DepthOfField.focalLength.value / m_DepthOfField.aperture.value;  // 조리개
    float P = m_DepthOfField.focusDistance.value;              // 초점 거리
    float maxCoC = (A * F) / (P - F);  // 최대 CoC 계산
    
    // 2. 보케 커널 생성 (육각형)
    Vector4[] bokehKernel = GenerateHexagonalKernel(
        m_DepthOfField.bladeCount.value, 
        m_DepthOfField.bladeCurvature.value);
    
    // 3. 5패스 구조 (Gaussian과 유사하지만 보케 블러 사용)
    using (var builder = renderGraph.AddUnsafePass<DoFBokehPassData>(
        "Depth of Field - Bokeh", out var passData))
    {
        passData.bokehKernel = bokehKernel;
        passData.cocParams = new Vector4(F, A, P, maxCoC);
        passData.downSample = 2;
        
        builder.SetRenderFunc(static (DoFBokehPassData data, UnsafeGraphContext context) =>
        {
            ExecuteBokehDoF(data, context);
        });
    }
}

private Vector4[] GenerateHexagonalKernel(int bladeCount, float curvature)
{
    // 육각형 보케 모양을 위한 샘플 포인트 생성
    var kernel = new Vector4[bladeCount * 2];  // 충분한 샘플 수
    
    for (int i = 0; i < kernel.Length; i++)
    {
        float angle = (float)i / kernel.Length * Mathf.PI * 2f;
        float radius = 1f;
        
        // 곡률 적용
        radius *= 1f - curvature * Mathf.Cos(angle * bladeCount);
        
        kernel[i] = new Vector4(
            Mathf.Cos(angle) * radius,
            Mathf.Sin(angle) * radius,
            0, 0
        );
    }
    
    return kernel;
}
```

---

## 텍스처 관리 전략

### 텍스처 생성 최적화

```csharp
public static class TextureCreationUtils
{
    // 표준 포스트프로세싱 텍스처 생성
    public static TextureHandle CreatePostProcessTexture(
        RenderGraph renderGraph,
        RenderTextureDescriptor baseDescriptor,
        int width, int height,
        GraphicsFormat format,
        string name,
        bool clear = true,
        FilterMode filterMode = FilterMode.Bilinear)
    {
        var desc = baseDescriptor;             // PostProcessPass.GetCompatibleDescriptor는 internal — 직접 구성
        desc.width           = width;
        desc.height          = height;
        desc.graphicsFormat  = format;
        desc.depthBufferBits = 0;
        
        // 포스트프로세싱에서는 MSAA 비활성화
        desc.msaaSamples = 1;
        
        return UniversalRenderer.CreateRenderGraphTexture(
            renderGraph, desc, name, clear, filterMode, TextureWrapMode.Clamp);
    }
    
    // 반해상도 텍스처 생성 (성능 최적화용)
    public static TextureHandle CreateHalfResTexture(
        RenderGraph renderGraph,
        RenderTextureDescriptor baseDescriptor,
        GraphicsFormat format,
        string name)
    {
        return CreatePostProcessTexture(
            renderGraph, baseDescriptor,
            Mathf.Max(1, baseDescriptor.width / 2),
            Mathf.Max(1, baseDescriptor.height / 2),
            format, name);
    }
    
    // CoC 전용 텍스처 (R16 포맷)
    public static TextureHandle CreateCoCTexture(
        RenderGraph renderGraph,
        RenderTextureDescriptor baseDescriptor,
        string name = "_CoCTexture")
    {
        return CreatePostProcessTexture(
            renderGraph, baseDescriptor,
            baseDescriptor.width, baseDescriptor.height,
            GraphicsFormat.R16_SFloat,  // CoC 값만 저장
            name);
    }
}
```

### 뷰포트 스케일링 처리

```csharp
public static class ViewportUtils
{
    public static Vector2 GetViewportScale(TextureHandle textureHandle)
    {
        RTHandle rtHandle = textureHandle;
        return rtHandle.useScaling ? 
            new Vector2(rtHandle.rtHandleProperties.rtHandleScale.x,
                       rtHandle.rtHandleProperties.rtHandleScale.y) : 
            Vector2.one;
    }
    
    public static void BlitWithViewportScale(CommandBuffer cmd, 
                                           TextureHandle source, 
                                           Material material, 
                                           int pass = 0)
    {
        RTHandle sourceHandle = source;
        Vector2 viewportScale = GetViewportScale(source);
        Blitter.BlitTexture(cmd, sourceHandle, viewportScale, material, pass);
    }
}
```

### 메모리 관리 베스트 프랙티스

```csharp
// ✅ 올바른 방법 - Transient 텍스처 사용
var tempTexture = UniversalRenderer.CreateRenderGraphTexture(
    renderGraph, desc, "_TempTexture", clear: true);
// RenderGraph가 자동으로 메모리 관리

// ❌ 잘못된 방법 - 수동 텍스처 생성 및 관리
var rt = new RenderTexture(width, height, 0, format);
// 수동으로 Release() 호출 필요, 메모리 누수 위험
```

---

## Volume System 통합

### VolumeComponent 구현

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Custom/My Effect")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
[URPHelpURL("post-processing-custom-effect")]  // 도움말 URL (선택사항)
public sealed class MyCustomEffect : VolumeComponent, IPostProcessComponent
{
    [Header("Main Parameters")]
    [Tooltip("Effect intensity")]
    public ClampedFloatParameter intensity = new ClampedFloatParameter(0f, 0f, 1f);
    
    [Tooltip("Enable high quality mode")]
    public BoolParameter highQuality = new BoolParameter(false);
    
    [Header("Color Parameters")]  
    [Tooltip("Effect color tint")]
    public ColorParameter tint = new ColorParameter(Color.white, true, true, true);
    
    [Header("Advanced")]
    [Tooltip("Custom texture")]
    public TextureParameter customTexture = new TextureParameter(null);
    
    [Tooltip("Blend mode")]
    public BlendModeParameter blendMode = new BlendModeParameter(BlendMode.Normal);
    
    // 효과 활성화 조건
    public bool IsActive()
    {
        return intensity.value > 0f;
    }
    
}

// 커스텀 파라미터 타입
[Serializable]
public sealed class BlendModeParameter : VolumeParameter<BlendMode>
{
    public BlendModeParameter(BlendMode value, bool overrideState = false) 
        : base(value, overrideState) { }
}

public enum BlendMode
{
    Normal,
    Add,
    Multiply,
    Screen,
    Overlay
}
```

### Volume 파라미터 타입들

```csharp
// 기본 제공 파라미터 타입들
public BoolParameter enableEffect = new BoolParameter(false);
public ClampedFloatParameter intensity = new ClampedFloatParameter(1f, 0f, 2f);
public MinFloatParameter minValue = new MinFloatParameter(0f, 0f);
public ClampedIntParameter sampleCount = new ClampedIntParameter(16, 8, 64);
public ColorParameter color = new ColorParameter(Color.white, true, true, true);
public Vector2Parameter offset = new Vector2Parameter(Vector2.zero);
public Vector3Parameter direction = new Vector3Parameter(Vector3.forward);
public Vector4Parameter parameters = new Vector4Parameter(Vector4.zero);
public TextureParameter texture = new TextureParameter(null);

// AnimationCurve와 그래디언트
public AnimationCurveParameter curve = new AnimationCurveParameter(AnimationCurve.Linear(0, 0, 1, 1));
public GradientParameter gradient = new GradientParameter(new Gradient());

// 커스텀 enum 파라미터
[Serializable]
public sealed class QualityParameter : VolumeParameter<QualityLevel>
{
    public QualityParameter(QualityLevel value, bool overrideState = false) 
        : base(value, overrideState) { }
}
```

---

## 필수 네임스페이스

### 완전한 using 문 리스트

```csharp
// Unity 기본
using System;
using UnityEngine;
using UnityEngine.Rendering;

// URP 코어
using UnityEngine.Rendering.Universal;

// RenderGraph (필수!)
using UnityEngine.Rendering.RenderGraphModule;

// URP 내부 (필요시)
using UnityEngine.Rendering.Universal.Internal;

// Volume System (VolumeComponent 사용시)
using UnityEngine.Rendering;

// 성능 최적화 (선택사항)
using Unity.Collections;
using Unity.Mathematics;
using Unity.Collections.LowLevel.Unsafe;

// 프로파일링 (선택사항)
using UnityEngine.Profiling;
```

### 자주 사용되는 유틸리티 클래스들

```csharp
// 블릿 작업
Blitter.BlitTexture(cmd, source, viewportScale, material, pass);
Blitter.BlitCameraTexture(cmd, source, destination, material, pass);

// 커맨드버퍼 유틸리티
var nativeCmd = CommandBufferHelpers.GetNativeCommandBuffer(context.cmd);

// 셰이더 키워드 관리
CoreUtils.SetKeyword(material, "_HIGH_QUALITY", enableHighQuality);
CoreUtils.SetKeyword(cmd, material, "_HIGH_QUALITY", enableHighQuality);

// 프로파일링
using (new ProfilingScope(cmd, ProfilingSampler.Get(URPProfileId.CustomEffect)))
{
    // 렌더링 작업
}

// 포스트프로세싱 유틸리티
PostProcessUtils.SetSourceSize(cmd, sourceTexture);
PostProcessUtils.ConfigureViewport(cmd, destination);

// 그래픽스 포맷 변환
var graphicsFormat = GraphicsFormatUtility.GetGraphicsFormat(RenderTextureFormat.DefaultHDR, false);
var linearFormat = GraphicsFormatUtility.GetLinearFormat(format);
var sRGBFormat = GraphicsFormatUtility.GetSRGBFormat(format);
```

---

## 실제 구현 예제

### 완전한 커스텀 포스트프로세싱 효과 구현

#### 1. Volume Component

```csharp
[Serializable, VolumeComponentMenu("Post-processing/Custom/Vintage Film")]
[SupportedOnRenderPipeline(typeof(UniversalRenderPipelineAsset))]
public sealed class VintageFilm : VolumeComponent, IPostProcessComponent
{
    [Header("Film Grain")]
    public ClampedFloatParameter grainIntensity = new ClampedFloatParameter(0f, 0f, 1f);
    public ClampedFloatParameter grainSize = new ClampedFloatParameter(1f, 0.1f, 3f);
    
    [Header("Vignette")]
    public ClampedFloatParameter vignetteIntensity = new ClampedFloatParameter(0f, 0f, 1f);
    public ClampedFloatParameter vignetteSmoothness = new ClampedFloatParameter(0.5f, 0f, 1f);
    
    [Header("Color Grading")]
    public ColorParameter tint = new ColorParameter(new Color(1f, 0.9f, 0.7f), false, false, true);
    public ClampedFloatParameter contrast = new ClampedFloatParameter(0f, -1f, 1f);
    
    [Header("Distortion")]
    public ClampedFloatParameter barrelDistortion = new ClampedFloatParameter(0f, -1f, 1f);
    
    public bool IsActive() => 
        grainIntensity.value > 0f || 
        vignetteIntensity.value > 0f || 
        !Mathf.Approximately(contrast.value, 0f) ||
        !Mathf.Approximately(barrelDistortion.value, 0f);
}
```

#### 2. Render Pass 구현

```csharp
public class VintageFilmRenderPass : ScriptableRenderPass
{
    private Material m_Material;
    private VintageFilm m_VintageFilm;
    
    private static readonly ProfilingSampler s_ProfilingSampler = 
        new ProfilingSampler("Vintage Film");
    
    private static readonly int s_GrainParams = Shader.PropertyToID("_GrainParams");
    private static readonly int s_VignetteParams = Shader.PropertyToID("_VignetteParams");
    private static readonly int s_ColorParams = Shader.PropertyToID("_ColorParams");
    private static readonly int s_DistortionParams = Shader.PropertyToID("_DistortionParams");
    
    public VintageFilmRenderPass(Material material)
    {
        m_Material = material;
        renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;
    }
    
    public void Setup(VintageFilm vintageFilm)
    {
        m_VintageFilm = vintageFilm;
    }
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        UniversalResourceData resourceData = frameData.Get<UniversalResourceData>();
        UniversalCameraData cameraData = frameData.Get<UniversalCameraData>();
        
        if (m_VintageFilm == null || !m_VintageFilm.IsActive())
            return;
            
        ExecuteVintageFilmEffect(renderGraph, resourceData, cameraData);
    }
    
    private void ExecuteVintageFilmEffect(RenderGraph renderGraph, 
                                        UniversalResourceData resourceData, 
                                        UniversalCameraData cameraData)
    {
        using (var builder = renderGraph.AddRasterRenderPass<VintageFilmPassData>(
            "Vintage Film Effect", out var passData, s_ProfilingSampler))
        {
            // 입력 텍스처
            passData.sourceTexture = resourceData.activeColorTexture;
            
            // 출력 텍스처 생성 (PostProcessPass.GetCompatibleDescriptor는 internal — 직접 구성)
            var outputDesc = cameraData.cameraTargetDescriptor;
            outputDesc.depthBufferBits = 0;
            outputDesc.msaaSamples    = 1;
            
            passData.destination = UniversalRenderer.CreateRenderGraphTexture(
                renderGraph, outputDesc, "_VintageFilmOutput", true);
            
            // 효과 파라미터
            passData.material = m_Material;
            passData.vintageFilm = m_VintageFilm;
            passData.screenSize = new Vector2(outputDesc.width, outputDesc.height);
            
            // 리소스 의존성
            builder.UseTexture(passData.sourceTexture, AccessFlags.Read);
            builder.SetRenderAttachment(passData.destination, 0, AccessFlags.Write);
            
            // 실행
            builder.SetRenderFunc(static (VintageFilmPassData data, RasterGraphContext context) =>
            {
                ExecutePass(data, context);
            });
        }
        
        // 결과를 activeColorTexture에 복사
        using (var copyBuilder = renderGraph.AddRasterRenderPass<BlitBackPassData>(
            "Blit Back To Active", out var blitBackData))
        {
            blitBackData.source = passData.destination;
            copyBuilder.UseTexture(blitBackData.source, AccessFlags.Read);
            copyBuilder.SetRenderAttachment(resourceData.activeColorTexture, 0, AccessFlags.WriteAll);
            copyBuilder.SetRenderFunc(static (BlitBackPassData d, RasterGraphContext ctx) =>
            {
                Blitter.BlitTexture(ctx.cmd, d.source, new Vector4(1f, 1f, 0f, 0f), 0, false);
            });
        }
    }
    
    private static void ExecutePass(VintageFilmPassData data, RasterGraphContext context)
    {
        var cmd = context.cmd;
        
        // 셰이더 파라미터 설정
        var grainParams = new Vector4(
            data.vintageFilm.grainIntensity.value,
            data.vintageFilm.grainSize.value,
            UnityEngine.Random.value * 1000f,  // 시간 기반 노이즈 시드
            0f
        );
        
        var vignetteParams = new Vector4(
            data.vintageFilm.vignetteIntensity.value,
            data.vintageFilm.vignetteSmoothness.value,
            0f, 0f
        );
        
        var colorParams = new Vector4(
            data.vintageFilm.tint.value.r,
            data.vintageFilm.tint.value.g,
            data.vintageFilm.tint.value.b,
            data.vintageFilm.contrast.value
        );
        
        var distortionParams = new Vector4(
            data.vintageFilm.barrelDistortion.value,
            data.screenSize.x / data.screenSize.y,  // aspect ratio
            0f, 0f
        );
        
        data.material.SetVector(s_GrainParams, grainParams);
        data.material.SetVector(s_VignetteParams, vignetteParams);
        data.material.SetVector(s_ColorParams, colorParams);
        data.material.SetVector(s_DistortionParams, distortionParams);
        
        // 키워드 설정
        CoreUtils.SetKeyword(data.material, "_GRAIN_ENABLED", 
            data.vintageFilm.grainIntensity.value > 0f);
        CoreUtils.SetKeyword(data.material, "_VIGNETTE_ENABLED", 
            data.vintageFilm.vignetteIntensity.value > 0f);
        CoreUtils.SetKeyword(data.material, "_DISTORTION_ENABLED", 
            !Mathf.Approximately(data.vintageFilm.barrelDistortion.value, 0f));
        
        // 블릿 실행
        ViewportUtils.BlitWithViewportScale(cmd, data.sourceTexture, data.material, 0);
    }
}

private class BlitBackPassData
{
    internal TextureHandle source;
}

private class VintageFilmPassData
{
    internal Material material;
    internal VintageFilm vintageFilm;
    internal TextureHandle sourceTexture;
    internal TextureHandle destination;
    internal Vector2 screenSize;
}
```

#### 3. Renderer Feature

```csharp
[DisallowMultipleRendererFeature("Vintage Film")]
public class VintageFilmRendererFeature : ScriptableRendererFeature
{
    [SerializeField] private Shader m_Shader;
    [SerializeField] private bool m_CreateMaterialInstance = true;
    
    private Material m_Material;
    private VintageFilmRenderPass m_RenderPass;
    
    public override void Create()
    {
        // 셰이더 유효성 검사
        if (m_Shader == null)
        {
            Debug.LogWarning("Vintage Film shader is missing!");
            return;
        }
        
        // 머티리얼 생성
        if (m_CreateMaterialInstance)
        {
            m_Material = CoreUtils.CreateEngineMaterial(m_Shader);
        }
        else
        {
            m_Material = new Material(m_Shader);
        }
        
        // 렌더 패스 생성
        m_RenderPass = new VintageFilmRenderPass(m_Material);
    }
    
    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        if (m_Material == null || m_RenderPass == null)
            return;
            
        // 게임 카메라에서만 실행
        if (renderingData.cameraData.camera.cameraType != CameraType.Game)
            return;
        
        // Volume에서 효과 설정 가져오기
        var stack = VolumeManager.instance.stack;
        var vintageFilm = stack.GetComponent<VintageFilm>();
        
        if (vintageFilm != null && vintageFilm.IsActive())
        {
            m_RenderPass.Setup(vintageFilm);
            renderer.EnqueuePass(m_RenderPass);
        }
    }
    
    protected override void Dispose(bool disposing)
    {
        if (m_Material != null)
        {
            if (m_CreateMaterialInstance)
            {
                CoreUtils.Destroy(m_Material);
            }
            else
            {
                DestroyImmediate(m_Material);
            }
        }
    }
}
```

#### 4. 셰이더 구현

```hlsl
Shader "Hidden/VintageFilm"
{
    Properties
    {
        [HideInInspector] _BlitTexture ("Source Texture", 2D) = "white" {}
        [HideInInspector] _GrainParams ("Grain Parameters", Vector) = (0,1,0,0)
        [HideInInspector] _VignetteParams ("Vignette Parameters", Vector) = (0,0.5,0,0)
        [HideInInspector] _ColorParams ("Color Parameters", Vector) = (1,0.9,0.7,0)
        [HideInInspector] _DistortionParams ("Distortion Parameters", Vector) = (0,1.77,0,0)
    }
    
    SubShader
    {
        Tags 
        { 
            "RenderType" = "Opaque" 
            "RenderPipeline" = "UniversalPipeline"
        }
        
        Cull Off 
        ZWrite Off 
        ZTest Always
        
        Pass
        {
            Name "VintageFilm"
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            // Feature keywords
            #pragma multi_compile_local _ _GRAIN_ENABLED
            #pragma multi_compile_local _ _VIGNETTE_ENABLED  
            #pragma multi_compile_local _ _DISTORTION_ENABLED
            
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl"
            
            TEXTURE2D_X(_BlitTexture);      // Blitter.BlitTexture는 _BlitTexture에 바인딩
            SAMPLER(sampler_BlitTexture);
            
            float4 _GrainParams;       // (intensity, size, seed, unused)
            float4 _VignetteParams;    // (intensity, smoothness, unused, unused)
            float4 _ColorParams;       // (tint.r, tint.g, tint.b, contrast)
            float4 _DistortionParams;  // (strength, aspectRatio, unused, unused)
            
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
            
            // 노이즈 함수
            float GradientNoise(float2 uv)
            {
                uv = uv * _GrainParams.y + _GrainParams.z;
                uv = fmod(uv, 289.0);
                float3 p = permute(permute(uv.y) + uv.x);
                return frac(p.z * (1.0/41.0)) * 2.0 - 1.0;
            }
            
            // 배럴 디스토션
            float2 BarrelDistortion(float2 uv, float strength)
            {
                float2 center = uv - 0.5;
                float r2 = dot(center, center);
                float distortion = 1.0 + strength * r2;
                return center * distortion + 0.5;
            }
            
            float4 frag(Varyings input) : SV_Target
            {
                float2 uv = input.texcoord;
                
                #ifdef _DISTORTION_ENABLED
                    uv = BarrelDistortion(uv, _DistortionParams.x);
                #endif
                
                // 소스 텍스처 샘플링
                float4 color = SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_BlitTexture, uv);
                
                // 색상 보정
                color.rgb *= _ColorParams.rgb;  // 틴트 적용
                
                // 대비 조정
                float contrast = _ColorParams.w;
                color.rgb = saturate((color.rgb - 0.5) * (1.0 + contrast) + 0.5);
                
                #ifdef _GRAIN_ENABLED
                    // 필름 그레인
                    float grain = GradientNoise(uv * _ScreenParams.xy);
                    color.rgb += grain * _GrainParams.x;
                #endif
                
                #ifdef _VIGNETTE_ENABLED
                    // 비네팅
                    float2 center = uv - 0.5;
                    float vignette = 1.0 - smoothstep(0.0, _VignetteParams.y, 
                        length(center) * _VignetteParams.x);
                    color.rgb *= vignette;
                #endif
                
                return color;
            }
            
            ENDHLSL
        }
    }
    
    FallBack "Hidden/Core/FallbackError"
}
```

---

## 성능 최적화

### 텍스처 포맷 최적화

```csharp
public static class OptimizedFormats
{
    // HDR 텍스처 포맷 선택
    public static GraphicsFormat GetOptimalHDRFormat()
    {
        // 플랫폼별 최적 포맷
        if (SystemInfo.IsFormatSupported(GraphicsFormat.B10G11R11_UFloatPack32, FormatUsage.Render))
            return GraphicsFormat.B10G11R11_UFloatPack32;  // 최고 성능
        else if (SystemInfo.IsFormatSupported(GraphicsFormat.R16G16B16A16_SFloat, FormatUsage.Render))
            return GraphicsFormat.R16G16B16A16_SFloat;      // 고품질
        else
            return GraphicsFormat.R32G32B32A32_SFloat;      // 폴백
    }
    
    // LDR 텍스처 포맷
    public static GraphicsFormat GetOptimalLDRFormat()
    {
        return GraphicsFormat.R8G8B8A8_SRGB;
    }
    
    // 단일 채널 텍스처 (CoC 등)
    public static GraphicsFormat GetOptimalSingleChannelFormat()
    {
        if (SystemInfo.IsFormatSupported(GraphicsFormat.R16_SFloat, FormatUsage.Render))
            return GraphicsFormat.R16_SFloat;
        else
            return GraphicsFormat.R32_SFloat;
    }
}
```

### 해상도 스케일링 전략

```csharp
public static class ResolutionScaling
{
    // 품질 레벨별 다운샘플링 비율
    public static int GetDownsampleFactor(PostProcessingQuality quality)
    {
        return quality switch
        {
            PostProcessingQuality.Low => 4,     // 1/4 해상도
            PostProcessingQuality.Medium => 2,  // 1/2 해상도  
            PostProcessingQuality.High => 1,    // 풀 해상도
            _ => 2
        };
    }
    
    // 적응형 품질 조정
    public static PostProcessingQuality GetAdaptiveQuality(RenderTextureDescriptor descriptor)
    {
        int pixelCount = descriptor.width * descriptor.height;
        
        // 해상도에 따른 자동 품질 조정
        if (pixelCount > 2073600)  // 1440p 이상
            return PostProcessingQuality.Medium;
        else if (pixelCount > 921600)  // 1080p 이상
            return PostProcessingQuality.High;
        else
            return PostProcessingQuality.High;  // 낮은 해상도에서는 고품질
    }
}

public enum PostProcessingQuality
{
    Low,
    Medium,
    High
}
```

### 셰이더 최적화 기법

```hlsl
// 성능 최적화된 셰이더 기법들

// 1. 조건문 최적화 - 키워드 사용
#pragma multi_compile_local _ _HIGH_QUALITY_MODE

#ifdef _HIGH_QUALITY_MODE
    // 고품질 샘플링
    color = HighQualitySampling(uv);
#else
    // 빠른 샘플링
    color = FastSampling(uv);
#endif

// 2. 텍스처 샘플링 최적화
// ❌ 비효율적
float4 color = 0;
for (int i = 0; i < sampleCount; i++)
{
    color += SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, uv + offsets[i]);
}

// ✅ 효율적 - 고정 언롤링
float4 color = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, uv + offsets[0]);
color += SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, uv + offsets[1]);
color += SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, uv + offsets[2]);
color += SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, uv + offsets[3]);

// 3. 수학 연산 최적화
// ❌ 비효율적
float distance = sqrt(dot(offset, offset));

// ✅ 효율적 - 제곱 거리 사용
float distanceSquared = dot(offset, offset);

// 4. 브랜치 최소화
// ❌ 브랜치 많음
if (intensity > 0.0)
{
    if (quality > 0.5)
        result = HighQualityEffect(uv);
    else
        result = LowQualityEffect(uv);
}

// ✅ 선형 보간 사용
float t = saturate(quality * 2.0);
float4 lowQuality = LowQualityEffect(uv);
float4 highQuality = HighQualityEffect(uv);
result = lerp(lowQuality, highQuality, t) * intensity;
```

---

## 문제해결 가이드

### 일반적인 컴파일 오류

#### 1. CS0452 - PassData reference type 오류
```
error CS0452: The type 'MyPassData' must be a reference type...
```

**해결방법**: PassData를 `class`로 정의
```csharp
// ❌ 
private struct MyPassData { }

// ✅
private class MyPassData { }
```

#### 2. CS0103 - GraphicsFormat 존재하지 않음
```
error CS0103: The name 'GraphicsFormat' does not exist in the current context
```

**해결방법**: 네임스페이스 추가
```csharp
using UnityEngine.Rendering;
```

#### 3. CS1061 - TextureDesc 변환 오류
```
error CS1503: Argument 1: cannot convert from 'UnityEngine.RenderTextureDescriptor' to 'TextureDesc'
```

**해결방법**: `UniversalRenderer.CreateRenderGraphTexture` 사용
```csharp
// ❌
TextureHandle texture = renderGraph.CreateTexture(renderTextureDescriptor);

// ✅  
TextureHandle texture = UniversalRenderer.CreateRenderGraphTexture(
    renderGraph, renderTextureDescriptor, "_TextureName", true);
```

#### 4. CS0029 - TextureHandle 할당 오류
```
error CS0029: Cannot implicitly convert type 'void' to 'TextureHandle'
```

**해결방법**: `UseTexture`는 의존성 선언용, 생성은 별도로
```csharp
// ❌
passData.sourceTexture = builder.UseTexture(sourceTexture, AccessFlags.Read);

// ✅
passData.sourceTexture = sourceTexture;
builder.UseTexture(sourceTexture, AccessFlags.Read);
```

### 런타임 문제 해결

#### 1. 검은 화면 출력
**원인**: 잘못된 뷰포트 스케일링
**해결방법**:
```csharp
Vector2 viewportScale = sourceHandle.useScaling ? 
    new Vector2(sourceHandle.rtHandleProperties.rtHandleScale.x,
               sourceHandle.rtHandleProperties.rtHandleScale.y) : 
    Vector2.one;
Blitter.BlitTexture(cmd, sourceHandle, viewportScale, material, 0);
```

#### 2. 메모리 누수
**원인**: 수동 텍스처 생성 및 해제 누락
**해결방법**: RenderGraph 자동 관리 사용
```csharp
// ✅ RenderGraph가 자동 관리
TextureHandle texture = UniversalRenderer.CreateRenderGraphTexture(/*...*/);
```

#### 3. 성능 저하
**원인**: 불필요한 텍스처 생성 및 과도한 해상도
**해결방법**: 품질별 최적화 적용
```csharp
int downsample = QualitySettings.GetQualityLevel() < 3 ? 2 : 1;
int width = cameraDescriptor.width / downsample;
int height = cameraDescriptor.height / downsample;
```

#### 4. Volume 효과 적용 안됨
**원인**: Volume 스택 구성 오류
**해결방법**: Volume 설정 검증
```csharp
var stack = VolumeManager.instance.stack;
var effect = stack.GetComponent<MyCustomEffect>();
if (effect != null && effect.IsActive() && effect.overrideState)
{
    // 효과 적용
}
```

### 디버깅 도구

#### 1. 텍스처 시각화
```csharp
#if UNITY_EDITOR
public static void DebugBlitToScreen(CommandBuffer cmd, TextureHandle texture, int quadrant = 0)
{
    var material = CoreUtils.CreateEngineMaterial("Hidden/DebugBlit");
    var rect = new Rect(quadrant * 0.25f, 0.75f, 0.25f, 0.25f);
    cmd.SetViewProjectionMatrices(Matrix4x4.identity, Matrix4x4.identity);
    cmd.DrawMesh(RenderingUtils.fullscreenMesh, Matrix4x4.identity, material);
}
#endif
```

#### 2. 성능 측정
```csharp
private static readonly ProfilerMarker s_EffectProfiler = 
    new ProfilerMarker("CustomEffect");

using (s_EffectProfiler.Auto())
{
    // 측정할 코드
}
```

#### 3. 파라미터 검증
```csharp
private void ValidateParameters()
{
    if (m_Material == null)
        Debug.LogError("Material is null!");
        
    if (!SystemInfo.IsFormatSupported(GraphicsFormat.B10G11R11_UFloatPack32, FormatUsage.Render))
        Debug.LogWarning("HDR format not supported, falling back to RGBA16");
}
```

---

## 피드백 및 개선점

### 현재 URP의 장점
1. **자동 메모리 관리**: RenderGraph의 Transient Resource 시스템으로 메모리 누수 방지
2. **최적화된 리소스 사용**: 자동 배칭 및 컬링으로 성능 향상
3. **강력한 Volume System**: 유연한 파라미터 관리 및 블렌딩
4. **크로스 플랫폼 호환성**: 모바일부터 고사양 PC까지 일관된 동작

### 개선이 필요한 부분

#### 1. 문서화 부족
- RenderGraph API의 세부 동작 방식 설명 부족
- PassData 설계 가이드라인 미제공
- 예제 코드의 복잡성으로 학습 곡선 가파름

#### 2. 디버깅 도구 한계
- 중간 텍스처 시각화 도구 부족
- 성능 병목 지점 식별 어려움
- Volume 파라미터 디버깅 불편

#### 3. API 일관성
- `AddRasterRenderPass`와 `AddUnsafePass`의 용도 구분이 모호
- 텍스처 생성 방법이 여러 개 존재하여 혼란
- 네임스페이스 분산으로 필수 import 파악 어려움

### 권장 개선사항

#### 1. 통합 텍스처 생성 API
```csharp
// 현재: 여러 방법 존재
UniversalRenderer.CreateRenderGraphTexture(/*...*/);
renderGraph.CreateTexture(/*...*/);

// 제안: 통합 API
TextureHandle texture = RenderGraphUtils.CreateTexture(/*...*/);
```

#### 2. 강화된 디버깅 지원
```csharp
#if UNITY_EDITOR
[System.Diagnostics.Conditional("UNITY_EDITOR")]
public static void DebugVisualize(TextureHandle texture, string name)
{
    // 자동으로 Scene View나 Game View에 시각화
}
#endif
```

#### 3. 표준화된 PassData 템플릿
```csharp
// 표준 PassData 베이스 클래스 제공
internal abstract class PostProcessPassData
{
    internal TextureHandle sourceTexture;
    internal TextureHandle destination;
    internal Material material;
    
    // 파생 클래스에서 추가 필드 정의
}
```

이 가이드는 Unity 6.0 URP RenderGraph API를 사용한 실제 프로덕션 환경에서의 포스트프로세싱 효과 구현을 위한 완전한 레퍼런스를 제공합니다.