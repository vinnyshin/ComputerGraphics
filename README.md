# 🎨 **3D Graphics Viewer**

> **OpenGL을 활용한 3D 그래픽 뷰어**
> 카메라 조작, 메쉬 렌더링, 계층적 애니메이션, BVH 모션 시각화를 지원하는 프로젝트

------

## 🚀 **프로젝트 개요**

이 프로젝트는 **OpenGL**을 이용하여 3D 모델을 로드하고 렌더링하는 **실시간 그래픽 뷰어**입니다.
**OBJ 파일 뷰어**와 **BVH 모션 뷰어**를 제공하며, **카메라 조작 및 조명 효과**도 지원합니다.

🎥 **데모 영상:**

- 🌀 **OBJ 애니메이션** → [🔗 YouTube](https://www.youtube.com/watch?v=3YkkPQo_g7U)
- 🏃 **BVH 모션 애니메이션** → [🔗 YouTube](https://youtu.be/hqVs3eyeYjg)

------

## 🛠 **기능 요약**

### ✨ **1. 기본 OpenGL 뷰어**

✔ **카메라 조작**: `Orbit`, `Panning`, `Zooming` 지원 (Blender와 유사한 방식)

✔ **그리드 표시**: XZ 평면 기준 격자 렌더링

✔ **투영 모드 전환**: `V` 키를 눌러 `원근(Perspective)` ↔ `직교(Orthogonal)` 전환

### 🎭 **2. OBJ 파일 뷰어**

✔ **단일 메쉬 렌더링 (Flat Shading)**

✔ **계층적 애니메이션 모델 (Hierarchical Animation)**

✔ **다중 광원 적용** (2개 이상의 광원 사용)

✔ **OBJ 파일 드래그 앤 드롭 로딩**

✔ **쉐이딩 모드 전환 (`S` 키) / 와이어프레임 모드 (`Z` 키)**

### 🏃 **3. BVH 파일 뷰어**

✔ **BVH 파일 드래그 앤 드롭 로딩**

✔ **스켈레톤(T-Pose) 렌더링 및 모션 애니메이션 (`Spacebar` 키로 재생)**

✔ **모션 데이터 출력 (프레임 수, FPS, 조인트 개수 등)**

✔ **박스 또는 OBJ 파일을 사용한 캐릭터 렌더링**

------

## 💻 **기술 스택**

- **언어**: `Python 3.7+`
- **라이브러리**: `OpenGL (PyOpenGL)`, `GLFW`, `NumPy`
- **렌더링 방식**: `glDrawArrays()`, `glDrawElements()`

------

## 🚀 **실행 방법**

1️⃣ **필수 라이브러리 설치**

```
pip install numpy glfw PyOpenGL
```

2️⃣ **프로그램 실행**

```
python main.py
```

3️⃣ **OBJ 또는 BVH 파일을 드래그 앤 드롭하여 로드**

4️⃣ **마우스 및 키보드 조작으로 3D 모델 탐색 및 애니메이션 실행**
