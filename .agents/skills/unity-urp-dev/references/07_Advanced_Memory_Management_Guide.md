# Unity 6.0 RenderGraph 고급 메모리 관리 가이드

## 개요

Unity 6.0 RenderGraph와 NativeContainer, unsafe 포인터를 활용한 고성능 메모리 관리 기법을 다룹니다. 상수버퍼 최적화, 제로 카피 데이터 전송, 그리고 동적 데이터 업데이트 없는 GPU 리소스 관리까지, 최고 수준의 성능 최적화 기법을 제공합니다.

## 목차

1. [Constant Buffer 고급 활용](#constant-buffer-고급-활용)
2. [NativeContainer 기반 데이터 관리](#nativecontainer-기반-데이터-관리)
3. [Unsafe 포인터와 제로 카피 전송](#unsafe-포인터와-제로-카피-전송)
4. [동적 상수버퍼 시스템](#동적-상수버퍼-시스템)
5. [GPU Persistent 데이터 관리](#gpu-persistent-데이터-관리)
6. [메모리 풀링과 생명주기](#메모리-풀링과-생명주기)
7. [RenderGraph 통합 패턴](#rendergraph-통합-패턴)
8. [성능 최적화 전략](#성능-최적화-전략)
9. [디버깅과 프로파일링](#디버깅과-프로파일링)
10. [실전 구현 예제](#실전-구현-예제)

---

## Constant Buffer 고급 활용

### 1. 계층적 상수버퍼 시스템

```csharp
using Unity.Collections;
using Unity.Collections.LowLevel.Unsafe;
using UnityEngine.Rendering;
using System;
using System.Runtime.InteropServices;

// GPU에서 사용하는 상수버퍼 레이아웃 (16바이트 정렬 필수)
[StructLayout(LayoutKind.Sequential, Pack = 16)]
public struct GlobalRenderingConstants
{
    public Matrix4x4 viewMatrix;           // 64 bytes
    public Matrix4x4 projMatrix;           // 64 bytes
    public Matrix4x4 viewProjMatrix;       // 64 bytes
    public Vector4 cameraPosition;         // 16 bytes
    public Vector4 screenParams;           // 16 bytes (width, height, 1/width, 1/height)
    public Vector4 timeParams;             // 16 bytes (time, deltaTime, frameCount, _)
    public float exposure;                 // 4 bytes
    public float gamma;                    // 4 bytes
    public int frameIndex;                 // 4 bytes
    public uint _padding;                  // 4 bytes (16바이트 정렬)
}

[StructLayout(LayoutKind.Sequential, Pack = 16)]
public struct PostProcessConstants
{
    public Vector4 bokehParams;            // (focusDistance, aperture, focalLength, maxCoC)
    public Vector4 filterParams;           // (angle, sampleCount, bladeCount, intensity)
    public Vector4 colorGradingParams;     // (contrast, saturation, brightness, _)
    public Vector4 lensParams;             // (distortion, chromaticAberration, vignette, _)
    public Matrix4x4 colorMatrix;          // 64 bytes
    public Vector4 temporalParams;         // (blendFactor, motionScale, historyWeight, _)
    public int qualityLevel;               // 4 bytes
    public uint enabledEffects;            // 4 bytes (비트 플래그)
    public uint _padding1;                 // 4 bytes
    public uint _padding2;                 // 4 bytes
}

// 고성능 상수버퍼 관리자
public unsafe class AdvancedConstantBufferManager : IDisposable
{
    private const int GLOBAL_CB_BINDING = 0;
    private const int POSTPROCESS_CB_BINDING = 1;
    private const int MAX_FRAMES_IN_FLIGHT = 3;
    
    // NativeContainer 기반 데이터 저장
    private NativeArray<GlobalRenderingConstants> m_GlobalConstants;
    private NativeArray<PostProcessConstants> m_PostProcessConstants;
    
    // GPU 상수버퍼
    private GraphicsBuffer[] m_GlobalConstantBuffers;
    private GraphicsBuffer[] m_PostProcessConstantBuffers;
    
    // 현재 프레임 인덱스 (트리플 버퍼링)
    private int m_CurrentFrameIndex;
    
    // Unsafe 포인터 캐시 (빠른 접근용)
    private GlobalRenderingConstants* m_GlobalPtr;
    private PostProcessConstants* m_PostProcessPtr;
    
    public AdvancedConstantBufferManager()
    {
        Initialize();
    }
    
    private void Initialize()
    {
        // NativeArray 생성 (Persistent 할당)
        m_GlobalConstants = new NativeArray<GlobalRenderingConstants>(
            MAX_FRAMES_IN_FLIGHT, Allocator.Persistent, NativeArrayOptions.ClearMemory);
        m_PostProcessConstants = new NativeArray<PostProcessConstants>(
            MAX_FRAMES_IN_FLIGHT, Allocator.Persistent, NativeArrayOptions.ClearMemory);
        
        // Unsafe 포인터 설정
        m_GlobalPtr = (GlobalRenderingConstants*)m_GlobalConstants.GetUnsafePtr();
        m_PostProcessPtr = (PostProcessConstants*)m_PostProcessConstants.GetUnsafePtr();
        
        // GPU 버퍼 생성 (각 프레임별)
        m_GlobalConstantBuffers = new GraphicsBuffer[MAX_FRAMES_IN_FLIGHT];
        m_PostProcessConstantBuffers = new GraphicsBuffer[MAX_FRAMES_IN_FLIGHT];
        
        for (int i = 0; i < MAX_FRAMES_IN_FLIGHT; i++)
        {
            m_GlobalConstantBuffers[i] = new GraphicsBuffer(
                GraphicsBuffer.Target.Constant,
                1, UnsafeUtility.SizeOf<GlobalRenderingConstants>());
                
            m_PostProcessConstantBuffers[i] = new GraphicsBuffer(
                GraphicsBuffer.Target.Constant,
                1, UnsafeUtility.SizeOf<PostProcessConstants>());
        }
        
        m_CurrentFrameIndex = 0;
    }
    
    // 제로 카피 데이터 업데이트 (포인터 직접 수정)
    public GlobalRenderingConstants* GetGlobalConstantsPtr()
    {
        return m_GlobalPtr + m_CurrentFrameIndex;
    }
    
    public PostProcessConstants* GetPostProcessConstantsPtr()
    {
        return m_PostProcessPtr + m_CurrentFrameIndex;
    }
    
    // 고속 데이터 업데이트 (memcpy 사용)
    public void UpdateGlobalConstants(in GlobalRenderingConstants constants)
    {
        var ptr = GetGlobalConstantsPtr();
        UnsafeUtility.CopyStructureToPtr(ref UnsafeUtility.AsRef<GlobalRenderingConstants>(in constants), ptr);
    }
    
    public void UpdatePostProcessConstants(in PostProcessConstants constants)
    {
        var ptr = GetPostProcessConstantsPtr();
        UnsafeUtility.CopyStructureToPtr(ref UnsafeUtility.AsRef<PostProcessConstants>(in constants), ptr);
    }
    
    // GPU로 데이터 전송 (NativeArray에서 직접)
    public void FlushToGPU()
    {
        int frameIndex = m_CurrentFrameIndex;
        
        // 전체 배열에서 현재 프레임만 추출하여 전송
        var globalSlice = m_GlobalConstants.GetSubArray(frameIndex, 1);
        var postProcessSlice = m_PostProcessConstants.GetSubArray(frameIndex, 1);
        
        m_GlobalConstantBuffers[frameIndex].SetData(globalSlice);
        m_PostProcessConstantBuffers[frameIndex].SetData(postProcessSlice);
    }
    
    // RenderGraph에서 사용할 버퍼 바인딩
    public void BindToRenderGraph(RenderGraph renderGraph, string passName)
    {
        int frameIndex = m_CurrentFrameIndex;
        
        // 전역 상수버퍼 바인딩
        var globalBufferHandle = renderGraph.ImportBuffer(m_GlobalConstantBuffers[frameIndex]);
        renderGraph.SetGlobalBuffer(passName + "_GlobalConstants", globalBufferHandle);
        
        // 포스트프로세스 상수버퍼 바인딩  
        var postProcessBufferHandle = renderGraph.ImportBuffer(m_PostProcessConstantBuffers[frameIndex]);
        renderGraph.SetGlobalBuffer(passName + "_PostProcessConstants", postProcessBufferHandle);
    }
    
    // 프레임 전환 (트리플 버퍼링)
    public void SwapFrame()
    {
        m_CurrentFrameIndex = (m_CurrentFrameIndex + 1) % MAX_FRAMES_IN_FLIGHT;
    }
    
    public void Dispose()
    {
        if (m_GlobalConstants.IsCreated) m_GlobalConstants.Dispose();
        if (m_PostProcessConstants.IsCreated) m_PostProcessConstants.Dispose();
        
        for (int i = 0; i < MAX_FRAMES_IN_FLIGHT; i++)
        {
            m_GlobalConstantBuffers?[i]?.Dispose();
            m_PostProcessConstantBuffers?[i]?.Dispose();
        }
    }
}
```

### 2. 동적 상수버퍼 헬퍼 클래스

```csharp
// 특정 효과를 위한 동적 상수버퍼
public unsafe class DynamicConstantBuffer<T> : IDisposable where T : unmanaged
{
    private NativeArray<T> m_Data;
    private GraphicsBuffer m_Buffer;
    private T* m_DataPtr;
    private bool m_IsDirty;
    
    public DynamicConstantBuffer(int capacity = 1)
    {
        m_Data = new NativeArray<T>(capacity, Allocator.Persistent);
        m_DataPtr = (T*)m_Data.GetUnsafePtr();
        
        m_Buffer = new GraphicsBuffer(
            GraphicsBuffer.Target.Constant,
            capacity, UnsafeUtility.SizeOf<T>());
        
        m_IsDirty = false;
    }
    
    // 포인터로 직접 접근 (가장 빠름)
    public T* GetDataPtr(int index = 0)
    {
        m_IsDirty = true;
        return m_DataPtr + index;
    }
    
    // 인덱서 접근
    public ref T this[int index]
    {
        get 
        { 
            m_IsDirty = true;
            return ref UnsafeUtility.ArrayElementAsRef<T>(m_DataPtr, index);
        }
    }
    
    // 배치 업데이트 (memcpy)
    public void UpdateRange(void* sourcePtr, int startIndex, int count)
    {
        var destPtr = m_DataPtr + startIndex;
        var size = UnsafeUtility.SizeOf<T>() * count;
        UnsafeUtility.MemCpy(destPtr, sourcePtr, size);
        m_IsDirty = true;
    }
    
    // 조건부 GPU 업데이트 (변경된 경우만)
    public void FlushIfDirty()
    {
        if (m_IsDirty)
        {
            m_Buffer.SetData(m_Data);
            m_IsDirty = false;
        }
    }
    
    public BufferHandle ImportToRenderGraph(RenderGraph renderGraph)
    {
        FlushIfDirty();
        return renderGraph.ImportBuffer(m_Buffer);
    }
    
    public void Dispose()
    {
        if (m_Data.IsCreated) m_Data.Dispose();
        m_Buffer?.Dispose();
    }
}
```

---

## NativeContainer 기반 데이터 관리

### 1. 고성능 데이터 컨테이너

```csharp
using Unity.Collections;
using Unity.Collections.LowLevel.Unsafe;
using Unity.Jobs;

// 멀티스레드 안전한 데이터 풀
[NativeContainer]
[NativeContainerIsAtomicWriteOnly]
public unsafe struct NativeDataPool<T> : IDisposable where T : unmanaged
{
    [NativeDisableUnsafePtrRestriction]
    private T* m_Buffer;
    private int m_Capacity;
    private int m_Count;
    private Allocator m_Allocator;
    
    // 원자적 카운터 (멀티스레드 안전)
    [NativeDisableUnsafePtrRestriction]
    private int* m_Counter;
    
#if ENABLE_UNITY_COLLECTIONS_CHECKS
    private AtomicSafetyHandle m_Safety;
    
    [NativeSetClassTypeToNullOnSchedule]
    private DisposeSentinel m_DisposeSentinel;
#endif
    
    public NativeDataPool(int capacity, Allocator allocator)
    {
        var size = UnsafeUtility.SizeOf<T>();
        var alignment = UnsafeUtility.AlignOf<T>();
        
        m_Buffer = (T*)UnsafeUtility.Malloc(size * capacity, alignment, allocator);
        m_Counter = (int*)UnsafeUtility.Malloc(sizeof(int), sizeof(int), allocator);
        *m_Counter = 0;
        
        m_Capacity = capacity;
        m_Count = 0;
        m_Allocator = allocator;
        
#if ENABLE_UNITY_COLLECTIONS_CHECKS
        DisposeSentinel.Create(out m_Safety, out m_DisposeSentinel, 1, allocator);
#endif
    }
    
    // 원자적 푸시 (멀티스레드 안전)
    public bool TryPush(T item)
    {
#if ENABLE_UNITY_COLLECTIONS_CHECKS
        AtomicSafetyHandle.CheckWriteAndThrow(m_Safety);
#endif
        
        int index = System.Threading.Interlocked.Increment(ref *m_Counter) - 1;
        if (index >= m_Capacity) return false;
        
        UnsafeUtility.WriteArrayElement(m_Buffer, index, item);
        m_Count = index + 1;
        return true;
    }
    
    // 원자적 팝
    public bool TryPop(out T item)
    {
#if ENABLE_UNITY_COLLECTIONS_CHECKS
        AtomicSafetyHandle.CheckWriteAndThrow(m_Safety);
#endif
        
        int index = System.Threading.Interlocked.Decrement(ref *m_Counter);
        if (index < 0)
        {
            System.Threading.Interlocked.Increment(ref *m_Counter);
            item = default;
            return false;
        }
        
        item = UnsafeUtility.ReadArrayElement<T>(m_Buffer, index);
        m_Count = index;
        return true;
    }
    
    // NativeArray로 변환 (제로 카피)
    public NativeArray<T> AsNativeArray()
    {
#if ENABLE_UNITY_COLLECTIONS_CHECKS
        AtomicSafetyHandle.CheckReadAndThrow(m_Safety);
#endif
        
        var array = NativeArrayUnsafeUtility.ConvertExistingDataToNativeArray<T>(
            m_Buffer, m_Count, m_Allocator);
            
#if ENABLE_UNITY_COLLECTIONS_CHECKS
        NativeArrayUnsafeUtility.SetAtomicSafetyHandle(ref array, m_Safety);
#endif
        
        return array;
    }
    
    // 포인터 직접 접근
    public T* GetUnsafePtr()
    {
#if ENABLE_UNITY_COLLECTIONS_CHECKS
        AtomicSafetyHandle.CheckWriteAndThrow(m_Safety);
#endif
        return m_Buffer;
    }
    
    public int Count => m_Count;
    public int Capacity => m_Capacity;
    
    public void Clear()
    {
        System.Threading.Interlocked.Exchange(ref *m_Counter, 0);
        m_Count = 0;
    }
    
    public void Dispose()
    {
#if ENABLE_UNITY_COLLECTIONS_CHECKS
        DisposeSentinel.Dispose(ref m_Safety, ref m_DisposeSentinel);
#endif
        
        if (m_Buffer != null)
        {
            UnsafeUtility.Free(m_Buffer, m_Allocator);
            UnsafeUtility.Free(m_Counter, m_Allocator);
            m_Buffer = null;
            m_Counter = null;
        }
    }
}

// 고성능 링버퍼 (순환 큐)
[NativeContainer]
public unsafe struct NativeRingBuffer<T> : IDisposable where T : unmanaged
{
    [NativeDisableUnsafePtrRestriction]
    private T* m_Buffer;
    private int m_Capacity;
    private int m_Head;
    private int m_Tail;
    private int m_Count;
    private Allocator m_Allocator;
    
#if ENABLE_UNITY_COLLECTIONS_CHECKS
    private AtomicSafetyHandle m_Safety;
    [NativeSetClassTypeToNullOnSchedule]
    private DisposeSentinel m_DisposeSentinel;
#endif
    
    public NativeRingBuffer(int capacity, Allocator allocator)
    {
        var size = UnsafeUtility.SizeOf<T>();
        var alignment = UnsafeUtility.AlignOf<T>();
        
        m_Buffer = (T*)UnsafeUtility.Malloc(size * capacity, alignment, allocator);
        m_Capacity = capacity;
        m_Head = 0;
        m_Tail = 0;
        m_Count = 0;
        m_Allocator = allocator;
        
#if ENABLE_UNITY_COLLECTIONS_CHECKS
        DisposeSentinel.Create(out m_Safety, out m_DisposeSentinel, 1, allocator);
#endif
    }
    
    public void Enqueue(T item)
    {
#if ENABLE_UNITY_COLLECTIONS_CHECKS
        AtomicSafetyHandle.CheckWriteAndThrow(m_Safety);
#endif
        
        UnsafeUtility.WriteArrayElement(m_Buffer, m_Tail, item);
        m_Tail = (m_Tail + 1) % m_Capacity;
        
        if (m_Count < m_Capacity)
            m_Count++;
        else
            m_Head = (m_Head + 1) % m_Capacity; // 오버플로우시 헤드 이동
    }
    
    public bool TryDequeue(out T item)
    {
#if ENABLE_UNITY_COLLECTIONS_CHECKS
        AtomicSafetyHandle.CheckWriteAndThrow(m_Safety);
#endif
        
        if (m_Count == 0)
        {
            item = default;
            return false;
        }
        
        item = UnsafeUtility.ReadArrayElement<T>(m_Buffer, m_Head);
        m_Head = (m_Head + 1) % m_Capacity;
        m_Count--;
        return true;
    }
    
    // 최신 N개 요소를 NativeArray로 반환
    public NativeArray<T> GetLatestN(int n, Allocator allocator)
    {
        n = Math.Min(n, m_Count);
        var result = new NativeArray<T>(n, allocator);
        
        for (int i = 0; i < n; i++)
        {
            int index = (m_Tail - n + i + m_Capacity) % m_Capacity;
            result[i] = UnsafeUtility.ReadArrayElement<T>(m_Buffer, index);
        }
        
        return result;
    }
    
    public int Count => m_Count;
    public int Capacity => m_Capacity;
    
    public void Dispose()
    {
#if ENABLE_UNITY_COLLECTIONS_CHECKS
        DisposeSentinel.Dispose(ref m_Safety, ref m_DisposeSentinel);
#endif
        
        if (m_Buffer != null)
        {
            UnsafeUtility.Free(m_Buffer, m_Allocator);
            m_Buffer = null;
        }
    }
}
```

### 2. 멀티스레드 데이터 프로세서

```csharp
// 멀티스레드 데이터 처리 Job
[BurstCompile(OptimizeFor = OptimizeFor.Performance)]
public struct ParallelDataProcessJob<T> : IJobParallelFor where T : unmanaged
{
    [ReadOnly] public NativeArray<T> input;
    [WriteOnly] public NativeArray<T> output;
    
    // 함수 포인터로 처리 로직 주입 (Burst 호환)
    [ReadOnly] public FunctionPointer<ProcessDelegate> processor;
    
    public delegate T ProcessDelegate(T input, int index);
    
    public void Execute(int index)
    {
        output[index] = processor.Invoke(input[index], index);
    }
}

// 실사용 예제
public class HighPerformanceDataProcessor
{
    private NativeDataPool<Vector4> m_InputPool;
    private NativeDataPool<Vector4> m_OutputPool;
    private NativeRingBuffer<Matrix4x4> m_TransformHistory;
    
    // Burst 컴파일된 처리 함수
    [BurstCompile]
    [MonoPInvokeCallback(typeof(ParallelDataProcessJob<Vector4>.ProcessDelegate))]
    static Vector4 ProcessVector(Vector4 input, int index)
    {
        // 고성능 벡터 변환
        return math.normalize(input) * math.length(input) * 0.5f;
    }
    
    public void ProcessDataParallel(NativeArray<Vector4> inputData)
    {
        var outputData = new NativeArray<Vector4>(inputData.Length, Allocator.TempJob);
        
        // 함수 포인터 생성
        var processorPtr = BurstCompiler.CompileFunctionPointer<ParallelDataProcessJob<Vector4>.ProcessDelegate>(ProcessVector);
        
        // 병렬 처리 Job 실행
        var job = new ParallelDataProcessJob<Vector4>
        {
            input = inputData,
            output = outputData,
            processor = processorPtr
        };
        
        var jobHandle = job.Schedule(inputData.Length, 64);
        jobHandle.Complete();
        
        // 결과를 풀에 저장
        for (int i = 0; i < outputData.Length; i++)
        {
            m_OutputPool.TryPush(outputData[i]);
        }
        
        outputData.Dispose();
    }
}
```

---

## Unsafe 포인터와 제로 카피 전송

### 1. 제로 카피 데이터 전송 시스템

```csharp
// GPU 메모리 직접 매핑
public unsafe class ZeroCopyBufferManager : IDisposable
{
    private GraphicsBuffer m_PersistentBuffer;
    private void* m_MappedMemory;
    private int m_BufferSize;
    private bool m_IsMapped;
    
    // 메모리 매핑을 통한 제로 카피 버퍼
    public void CreateMappedBuffer<T>(int elementCount) where T : unmanaged
    {
        m_BufferSize = UnsafeUtility.SizeOf<T>() * elementCount;
        
        // GPU 버퍼 생성 (CPU에서 읽기/쓰기 가능)
        m_PersistentBuffer = new GraphicsBuffer(
            GraphicsBuffer.Target.Structured,
            elementCount,
            UnsafeUtility.SizeOf<T>()
        );
        
        // 메모리 매핑 시도 (플랫폼에 따라 지원 여부 다름)
        if (SystemInfo.graphicsMemorySize > 0)
        {
            m_MappedMemory = MapGPUMemory();
            m_IsMapped = m_MappedMemory != null;
        }
    }
    
    // 플랫폼별 메모리 매핑 구현
    private void* MapGPUMemory()
    {
        // DirectX 12에서 메모리 매핑
        #if UNITY_STANDALONE_WIN && !UNITY_EDITOR
        // D3D12 메모리 매핑 구현
        return MapD3D12Memory();
        #elif UNITY_STANDALONE_OSX
        // Metal 메모리 매핑 구현
        return MapMetalMemory();
        #else
        // 매핑 지원하지 않음
        return null;
        #endif
    }
    
    // 직접 포인터 접근 (매핑된 경우)
    public T* GetDirectPtr<T>() where T : unmanaged
    {
        if (!m_IsMapped) return null;
        return (T*)m_MappedMemory;
    }
    
    // NativeArray 래핑 (제로 카피)
    public NativeArray<T> GetNativeArrayView<T>() where T : unmanaged
    {
        if (!m_IsMapped)
        {
            // 매핑되지 않은 경우 일반적인 방법 사용
            var tempData = new NativeArray<T>(m_BufferSize / UnsafeUtility.SizeOf<T>(), 
                                             Allocator.Temp);
            m_PersistentBuffer.GetData(tempData);
            return tempData;
        }
        
        // 매핑된 메모리를 NativeArray로 래핑
        var array = NativeArrayUnsafeUtility.ConvertExistingDataToNativeArray<T>(
            m_MappedMemory, m_BufferSize / UnsafeUtility.SizeOf<T>(), Allocator.None);
            
        #if ENABLE_UNITY_COLLECTIONS_CHECKS
        // 안전성 핸들 설정
        var safety = AtomicSafetyHandle.Create();
        NativeArrayUnsafeUtility.SetAtomicSafetyHandle(ref array, safety);
        #endif
        
        return array;
    }
    
    // 고속 메모리 복사 (SIMD 최적화)
    public void FastCopy<T>(T* source, int count) where T : unmanaged
    {
        var destination = GetDirectPtr<T>();
        if (destination == null)
        {
            // 매핑되지 않은 경우 일반 SetData 사용
            var tempArray = NativeArrayUnsafeUtility.ConvertExistingDataToNativeArray<T>(
                source, count, Allocator.None);
            m_PersistentBuffer.SetData(tempArray);
            return;
        }
        
        // 직접 메모리 복사 (가장 빠름)
        var size = UnsafeUtility.SizeOf<T>() * count;
        UnsafeUtility.MemCpy(destination, source, size);
    }
    
    // 비동기 복사
    public JobHandle FastCopyAsync<T>(T* source, int count) where T : unmanaged
    {
        var job = new MemCopyJob
        {
            source = source,
            destination = GetDirectPtr<T>(),
            size = UnsafeUtility.SizeOf<T>() * count
        };
        
        return job.Schedule();
    }
    
    public void Dispose()
    {
        if (m_IsMapped && m_MappedMemory != null)
        {
            UnmapGPUMemory();
            m_MappedMemory = null;
        }
        
        m_PersistentBuffer?.Dispose();
    }
}

// 고속 메모리 복사 Job (Burst 최적화)
[BurstCompile(OptimizeFor = OptimizeFor.Performance)]
public unsafe struct MemCopyJob : IJob
{
    [NativeDisableUnsafePtrRestriction]
    public void* source;
    
    [NativeDisableUnsafePtrRestriction] 
    public void* destination;
    
    public long size;
    
    public void Execute()
    {
        // Burst가 SIMD로 최적화
        UnsafeUtility.MemCpy(destination, source, size);
    }
}
```

### 2. 스트리밍 데이터 업데이트

```csharp
// 스트리밍 방식의 동적 버퍼 업데이트
public unsafe class StreamingBufferUpdater<T> : IDisposable where T : unmanaged
{
    private const int RING_BUFFER_SIZE = 4;
    
    // 링 버퍼로 구성된 스트리밍 버퍼들
    private GraphicsBuffer[] m_StreamingBuffers;
    private NativeArray<T>[] m_StagingBuffers;
    private T*[] m_StagingPtrs;
    
    private int m_CurrentBuffer;
    private int m_ElementCount;
    private bool m_IsStreaming;
    
    public StreamingBufferUpdater(int elementCount)
    {
        m_ElementCount = elementCount;
        Initialize();
    }
    
    private void Initialize()
    {
        m_StreamingBuffers = new GraphicsBuffer[RING_BUFFER_SIZE];
        m_StagingBuffers = new NativeArray<T>[RING_BUFFER_SIZE];
        m_StagingPtrs = new T*[RING_BUFFER_SIZE];
        
        var elementSize = UnsafeUtility.SizeOf<T>();
        
        for (int i = 0; i < RING_BUFFER_SIZE; i++)
        {
            // GPU 버퍼 생성
            m_StreamingBuffers[i] = new GraphicsBuffer(
                GraphicsBuffer.Target.Structured,
                m_ElementCount, elementSize);
            
            // CPU 스테이징 버퍼
            m_StagingBuffers[i] = new NativeArray<T>(m_ElementCount, 
                Allocator.Persistent, NativeArrayOptions.UninitializedMemory);
            
            // Unsafe 포인터 캐시
            m_StagingPtrs[i] = (T*)m_StagingBuffers[i].GetUnsafePtr();
        }
        
        m_CurrentBuffer = 0;
        m_IsStreaming = false;
    }
    
    // 현재 프레임의 쓰기용 포인터 반환
    public T* BeginWrite()
    {
        // 다음 버퍼로 전환 (이전 버퍼는 GPU가 사용 중일 수 있음)
        m_CurrentBuffer = (m_CurrentBuffer + 1) % RING_BUFFER_SIZE;
        m_IsStreaming = true;
        
        return m_StagingPtrs[m_CurrentBuffer];
    }
    
    // 배치 쓰기 (인덱스 범위)
    public void WriteBatch(int startIndex, T* sourceData, int count)
    {
        if (!m_IsStreaming) return;
        
        var destPtr = m_StagingPtrs[m_CurrentBuffer] + startIndex;
        var size = UnsafeUtility.SizeOf<T>() * count;
        UnsafeUtility.MemCpy(destPtr, sourceData, size);
    }
    
    // 단일 요소 쓰기 (인라인 최적화)
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public void WriteElement(int index, in T value)
    {
        if (!m_IsStreaming) return;
        m_StagingPtrs[m_CurrentBuffer][index] = value;
    }
    
    // GPU로 전송 완료
    public GraphicsBuffer EndWrite()
    {
        if (!m_IsStreaming) return null;
        
        // 현재 스테이징 버퍼를 GPU로 전송
        m_StreamingBuffers[m_CurrentBuffer].SetData(m_StagingBuffers[m_CurrentBuffer]);
        m_IsStreaming = false;
        
        return m_StreamingBuffers[m_CurrentBuffer];
    }
    
    // 비동기 업데이트 (Job 사용)
    public JobHandle BeginAsyncWrite(JobHandle dependency = default)
    {
        m_CurrentBuffer = (m_CurrentBuffer + 1) % RING_BUFFER_SIZE;
        return dependency; // 추가 처리를 위해 dependency 체인 반환
    }
    
    public JobHandle WriteAsync<TJob>(TJob job, JobHandle dependency = default) 
        where TJob : struct, IJob
    {
        return job.Schedule(dependency);
    }
    
    public GraphicsBuffer EndAsyncWrite(JobHandle jobHandle)
    {
        jobHandle.Complete();
        return EndWrite();
    }
    
    public void Dispose()
    {
        for (int i = 0; i < RING_BUFFER_SIZE; i++)
        {
            m_StreamingBuffers[i]?.Dispose();
            if (m_StagingBuffers[i].IsCreated)
                m_StagingBuffers[i].Dispose();
        }
    }
}
```

---

## 동적 상수버퍼 시스템

### 1. 자동 업데이트 상수버퍼

```csharp
// 변경 감지 및 자동 업데이트 상수버퍼
public unsafe class AutoUpdateConstantBuffer<T> : IDisposable where T : unmanaged
{
    private NativeArray<T> m_CurrentData;
    private NativeArray<T> m_PreviousData;
    private GraphicsBuffer m_ConstantBuffer;
    private T* m_CurrentPtr;
    private T* m_PreviousPtr;
    private uint m_CurrentHash;
    private bool m_ForceUpdate;
    
    public AutoUpdateConstantBuffer()
    {
        Initialize();
    }
    
    private void Initialize()
    {
        m_CurrentData = new NativeArray<T>(1, Allocator.Persistent);
        m_PreviousData = new NativeArray<T>(1, Allocator.Persistent);
        
        m_CurrentPtr = (T*)m_CurrentData.GetUnsafePtr();
        m_PreviousPtr = (T*)m_PreviousData.GetUnsafePtr();
        
        m_ConstantBuffer = new GraphicsBuffer(
            GraphicsBuffer.Target.Constant, 1, UnsafeUtility.SizeOf<T>());
        
        m_CurrentHash = 0;
        m_ForceUpdate = true;
    }
    
    // 데이터 포인터 접근 (자동으로 더티 마킹)
    public T* GetDataPtr()
    {
        return m_CurrentPtr;
    }
    
    // 참조로 접근
    public ref T Data => ref UnsafeUtility.AsRef<T>(m_CurrentPtr);
    
    // 해시 기반 변경 감지
    private bool HasDataChanged()
    {
        if (m_ForceUpdate) return true;
        
        // 빠른 해시 계산 (xxHash 또는 유사 알고리즘)
        uint newHash = CalculateHash(m_CurrentPtr);
        bool changed = newHash != m_CurrentHash;
        m_CurrentHash = newHash;
        
        return changed;
    }
    
    // 고속 해시 계산 (Burst 최적화)
    [BurstCompile]
    private static uint CalculateHash(T* data)
    {
        // xxHash32 간소화 버전
        var bytes = (byte*)data;
        var size = UnsafeUtility.SizeOf<T>();
        
        uint hash = 2654435761U;
        for (int i = 0; i < size; i += 4)
        {
            uint chunk = *(uint*)(bytes + i);
            hash ^= chunk;
            hash *= 2654435761U;
            hash ^= hash >> 16;
        }
        
        return hash;
    }
    
    // 조건부 GPU 업데이트
    public bool UpdateIfChanged()
    {
        if (!HasDataChanged()) return false;
        
        m_ConstantBuffer.SetData(m_CurrentData);
        
        // 이전 데이터 백업
        UnsafeUtility.MemCpy(m_PreviousPtr, m_CurrentPtr, UnsafeUtility.SizeOf<T>());
        m_ForceUpdate = false;
        
        return true;
    }
    
    // 강제 업데이트
    public void ForceUpdate()
    {
        m_ForceUpdate = true;
        UpdateIfChanged();
    }
    
    public BufferHandle ImportToRenderGraph(RenderGraph renderGraph)
    {
        UpdateIfChanged();
        return renderGraph.ImportBuffer(m_ConstantBuffer);
    }
    
    public void Dispose()
    {
        if (m_CurrentData.IsCreated) m_CurrentData.Dispose();
        if (m_PreviousData.IsCreated) m_PreviousData.Dispose();
        m_ConstantBuffer?.Dispose();
    }
}

// 멀티 프레임 상수버퍼 (히스토리 관리)
public unsafe class HistoryConstantBuffer<T> : IDisposable where T : unmanaged
{
    private const int MAX_HISTORY = 8;
    
    private NativeRingBuffer<T> m_History;
    private GraphicsBuffer m_HistoryBuffer;
    private T* m_CurrentPtr;
    
    public HistoryConstantBuffer()
    {
        m_History = new NativeRingBuffer<T>(MAX_HISTORY, Allocator.Persistent);
        m_HistoryBuffer = new GraphicsBuffer(
            GraphicsBuffer.Target.Structured, MAX_HISTORY, UnsafeUtility.SizeOf<T>());
    }
    
    // 새 프레임 데이터 추가
    public void PushFrame(in T frameData)
    {
        m_History.Enqueue(frameData);
        
        // 전체 히스토리를 GPU로 전송
        var historyArray = m_History.GetLatestN(MAX_HISTORY, Allocator.Temp);
        m_HistoryBuffer.SetData(historyArray);
        historyArray.Dispose();
    }
    
    // N 프레임 전 데이터 가져오기
    public T GetFrameData(int framesBack)
    {
        var historyArray = m_History.GetLatestN(framesBack + 1, Allocator.Temp);
        T result = historyArray.Length > framesBack ? historyArray[0] : default;
        historyArray.Dispose();
        return result;
    }
    
    public BufferHandle ImportToRenderGraph(RenderGraph renderGraph)
    {
        return renderGraph.ImportBuffer(m_HistoryBuffer);
    }
    
    public void Dispose()
    {
        m_History.Dispose();
        m_HistoryBuffer?.Dispose();
    }
}
```

---

## GPU Persistent 데이터 관리

### 1. 영구 GPU 리소스 관리자

```csharp
// GPU 메모리에 영구적으로 상주하는 데이터 관리
public unsafe class PersistentGPUDataManager : IDisposable
{
    private Dictionary<string, PersistentBuffer> m_PersistentBuffers;
    private Dictionary<string, WeakReference> m_DataReferences;
    
    private struct PersistentBuffer
    {
        public GraphicsBuffer buffer;
        public void* mappedMemory;
        public int elementCount;
        public int elementSize;
        public Type dataType;
    }
    
    public PersistentGPUDataManager()
    {
        m_PersistentBuffers = new Dictionary<string, PersistentBuffer>();
        m_DataReferences = new Dictionary<string, WeakReference>();
    }
    
    // 영구 버퍼 등록
    public void RegisterPersistentBuffer<T>(string name, int elementCount) where T : unmanaged
    {
        if (m_PersistentBuffers.ContainsKey(name)) return;
        
        var elementSize = UnsafeUtility.SizeOf<T>();
        var buffer = new GraphicsBuffer(
            GraphicsBuffer.Target.Structured, elementCount, elementSize);
        
        // 메모리 매핑 시도
        void* mappedMemory = null;
        if (SystemInfo.graphicsMemorySize > 0)
        {
            mappedMemory = TryMapBuffer(buffer);
        }
        
        m_PersistentBuffers[name] = new PersistentBuffer
        {
            buffer = buffer,
            mappedMemory = mappedMemory,
            elementCount = elementCount,
            elementSize = elementSize,
            dataType = typeof(T)
        };
    }
    
    // 데이터 포인터 참조 (매핑된 메모리)
    public T* GetPersistentPtr<T>(string name) where T : unmanaged
    {
        if (!m_PersistentBuffers.TryGetValue(name, out var persistentBuffer))
            return null;
            
        if (persistentBuffer.dataType != typeof(T))
            return null;
            
        return (T*)persistentBuffer.mappedMemory;
    }
    
    // NativeArray 뷰 생성 (제로 카피)
    public NativeArray<T> GetPersistentArray<T>(string name) where T : unmanaged
    {
        var ptr = GetPersistentPtr<T>(name);
        if (ptr == null) return default;
        
        var persistentBuffer = m_PersistentBuffers[name];
        var array = NativeArrayUnsafeUtility.ConvertExistingDataToNativeArray<T>(
            ptr, persistentBuffer.elementCount, Allocator.None);
            
        #if ENABLE_UNITY_COLLECTIONS_CHECKS
        var safety = AtomicSafetyHandle.Create();
        NativeArrayUnsafeUtility.SetAtomicSafetyHandle(ref array, safety);
        #endif
        
        return array;
    }
    
    // 데이터 참조 관리 (약한 참조로 메모리 누수 방지)
    public PersistentDataRef<T> GetDataReference<T>(string name) where T : unmanaged
    {
        if (m_DataReferences.TryGetValue(name, out var weakRef))
        {
            if (weakRef.Target is PersistentDataRef<T> existingRef)
                return existingRef;
        }
        
        var dataRef = new PersistentDataRef<T>(this, name);
        m_DataReferences[name] = new WeakReference(dataRef);
        return dataRef;
    }
    
    // RenderGraph 통합
    public BufferHandle ImportToRenderGraph(string name, RenderGraph renderGraph)
    {
        if (m_PersistentBuffers.TryGetValue(name, out var persistentBuffer))
        {
            return renderGraph.ImportBuffer(persistentBuffer.buffer);
        }
        
        return new BufferHandle();
    }
    
    public void Dispose()
    {
        foreach (var kvp in m_PersistentBuffers)
        {
            var buffer = kvp.Value;
            if (buffer.mappedMemory != null)
            {
                UnmapBuffer(buffer.buffer);
            }
            buffer.buffer?.Dispose();
        }
        
        m_PersistentBuffers.Clear();
        m_DataReferences.Clear();
    }
    
    private void* TryMapBuffer(GraphicsBuffer buffer)
    {
        // 플랫폼별 버퍼 매핑 구현
        return null; // 구현 필요
    }
    
    private void UnmapBuffer(GraphicsBuffer buffer)
    {
        // 매핑 해제 구현
    }
}

// 영구 데이터 참조 (RAII 패턴)
public unsafe struct PersistentDataRef<T> : IDisposable where T : unmanaged
{
    private PersistentGPUDataManager m_Manager;
    private string m_Name;
    private T* m_DataPtr;
    
    internal PersistentDataRef(PersistentGPUDataManager manager, string name)
    {
        m_Manager = manager;
        m_Name = name;
        m_DataPtr = manager.GetPersistentPtr<T>(name);
    }
    
    // 데이터 포인터 접근
    public T* Ptr => m_DataPtr;
    
    // 인덱서 접근
    public ref T this[int index] => ref m_DataPtr[index];
    
    // RenderGraph 통합
    public BufferHandle ImportToRenderGraph(RenderGraph renderGraph)
    {
        return m_Manager.ImportToRenderGraph(m_Name, renderGraph);
    }
    
    public void Dispose()
    {
        // 명시적 해제는 불필요 (영구 데이터)
        m_DataPtr = null;
        m_Manager = null;
        m_Name = null;
    }
}
```

---

## RenderGraph 통합 패턴

### 1. 고급 RenderGraph 상수버퍼 패스

```csharp
// RenderGraph와 완전히 통합된 상수버퍼 관리
public class RenderGraphConstantBufferPass : ScriptableRenderPass
{
    private AdvancedConstantBufferManager m_CBManager;
    private PersistentGPUDataManager m_PersistentManager;
    private Dictionary<string, IConstantBufferUpdater> m_Updaters;
    
    public interface IConstantBufferUpdater
    {
        void UpdateConstants(unsafe void* dataPtr, int frameIndex);
        Type GetDataType();
        int GetDataSize();
    }
    
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        // 모든 상수버퍼 업데이터 실행
        ExecuteConstantBufferUpdates(frameData);
        
        // RenderGraph에 리소스 등록
        RegisterConstantBuffers(renderGraph);
        
        // 포스트프로세싱 패스들에 상수버퍼 바인딩
        ExecutePostProcessPasses(renderGraph, frameData);
    }
    
    private unsafe void ExecuteConstantBufferUpdates(ContextContainer frameData)
    {
        var cameraData = frameData.Get<UniversalCameraData>();
        var timeData = frameData.Get<UniversalTimeData>();
        
        // 전역 상수 업데이트
        var globalPtr = m_CBManager.GetGlobalConstantsPtr();
        UpdateGlobalConstants(globalPtr, cameraData, timeData);
        
        // 포스트프로세스 상수 업데이트
        var postProcessPtr = m_CBManager.GetPostProcessConstantsPtr();
        UpdatePostProcessConstants(postProcessPtr, frameData);
        
        // 커스텀 업데이터들 실행
        int frameIndex = Time.frameCount % 3;
        foreach (var kvp in m_Updaters)
        {
            var updater = kvp.Value;
            var dataType = updater.GetDataType();
            var dataSize = updater.GetDataSize();
            
            // 스택 할당된 임시 버퍼 사용
            var tempBuffer = stackalloc byte[dataSize];
            updater.UpdateConstants(tempBuffer, frameIndex);
            
            // 영구 버퍼에 복사
            var persistentPtr = m_PersistentManager.GetPersistentPtr<byte>(kvp.Key);
            if (persistentPtr != null)
            {
                UnsafeUtility.MemCpy(persistentPtr, tempBuffer, dataSize);
            }
        }
        
        // GPU로 전송
        m_CBManager.FlushToGPU();
    }
    
    private unsafe void UpdateGlobalConstants(GlobalRenderingConstants* constants, 
                                            UniversalCameraData cameraData,
                                            UniversalTimeData timeData)
    {
        // 직접 포인터 수정 (가장 빠름)
        constants->viewMatrix = cameraData.GetViewMatrix();
        constants->projMatrix = cameraData.GetProjectionMatrix();
        constants->viewProjMatrix = cameraData.GetGPUProjectionMatrix() * cameraData.GetViewMatrix();
        constants->cameraPosition = cameraData.worldSpaceCameraPos;
        
        constants->screenParams = new Vector4(
            cameraData.cameraTargetDescriptor.width,
            cameraData.cameraTargetDescriptor.height,
            1.0f / cameraData.cameraTargetDescriptor.width,
            1.0f / cameraData.cameraTargetDescriptor.height
        );
        
        constants->timeParams = new Vector4(
            timeData.time, timeData.deltaTime, Time.frameCount, 0
        );
        
        constants->frameIndex = Time.frameCount;
    }
    
    private void RegisterConstantBuffers(RenderGraph renderGraph)
    {
        // 전역 상수버퍼 등록
        m_CBManager.BindToRenderGraph(renderGraph, "Global");
        
        // 영구 버퍼들 등록
        foreach (var bufferName in GetRegisteredBufferNames())
        {
            m_PersistentManager.ImportToRenderGraph(bufferName, renderGraph);
        }
    }
    
    private void ExecutePostProcessPasses(RenderGraph renderGraph, ContextContainer frameData)
    {
        var resourceData = frameData.Get<UniversalResourceData>();
        
        // 다중 패스 포스트프로세싱 (상수버퍼 공유)
        using (var passGroup = renderGraph.CreatePassGroup("Post Process Chain"))
        {
            TextureHandle currentInput = resourceData.activeColorTexture;
            
            // 각 패스에서 동일한 상수버퍼 세트 사용
            var sharedConstants = GetSharedConstantBuffers(renderGraph);
            
            currentInput = ExecuteBokehPass(renderGraph, currentInput, sharedConstants);
            currentInput = ExecuteColorGradingPass(renderGraph, currentInput, sharedConstants);
            currentInput = ExecuteTAAPass(renderGraph, currentInput, sharedConstants);
            
            // 최종 결과 복사
            CopyToActiveTexture(renderGraph, currentInput, resourceData);
        }
    }
    
    private SharedConstantBuffers GetSharedConstantBuffers(RenderGraph renderGraph)
    {
        return new SharedConstantBuffers
        {
            globalConstants = renderGraph.ImportBuffer(m_CBManager.GetGlobalBuffer()),
            postProcessConstants = renderGraph.ImportBuffer(m_CBManager.GetPostProcessBuffer()),
            persistentData = m_PersistentManager.ImportToRenderGraph("PersistentData", renderGraph)
        };
    }
    
    private struct SharedConstantBuffers
    {
        public BufferHandle globalConstants;
        public BufferHandle postProcessConstants;
        public BufferHandle persistentData;
    }
}

// 특정 효과용 상수버퍼 업데이터 예제
public class BokehConstantBufferUpdater : IConstantBufferUpdater
{
    [StructLayout(LayoutKind.Sequential, Pack = 16)]
    struct BokehConstants
    {
        public Vector4 focusParams;
        public Vector4 filterParams;
        public Matrix4x4 sampleOffsets;
    }
    
    public unsafe void UpdateConstants(void* dataPtr, int frameIndex)
    {
        var constants = (BokehConstants*)dataPtr;
        var volume = VolumeManager.instance.stack.GetComponent<PolygonalBokehVolume>();
        
        if (volume != null && volume.IsActive())
        {
            constants->focusParams = new Vector4(
                volume.focusDistance.value,
                volume.aperture.value,
                volume.focalLength.value,
                volume.maxCoC.value
            );
            
            // 프레임별 지터 적용
            var jitter = GetFrameJitter(frameIndex);
            constants->filterParams = new Vector4(
                GetBokehAngle(volume.bokehShape.value),
                GetSampleCount(volume.quality.value),
                GetBladeCount(volume.bokehShape.value),
                volume.intensity.value + jitter
            );
        }
    }
    
    public Type GetDataType() => typeof(BokehConstants);
    public int GetDataSize() => UnsafeUtility.SizeOf<BokehConstants>();
    
    private float GetFrameJitter(int frameIndex)
    {
        // 시간에 따른 지터로 노이즈 감소
        return Mathf.Sin(frameIndex * 0.1f) * 0.001f;
    }
}
```

이 고급 메모리 관리 가이드는 Unity 6.0 RenderGraph에서 최고 성능을 달성하기 위한 전문적인 기법들을 다룹니다. NativeContainer, unsafe 포인터, 제로 카피 전송을 활용하여 CPU-GPU 간 데이터 전송 오버헤드를 최소화하고, 동적 업데이트 없이도 효율적인 데이터 관리가 가능한 시스템을 구축할 수 있습니다.