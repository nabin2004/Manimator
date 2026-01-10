from src.manimator.planner.scene_planner import plan_scene
from src.manimator.codegen.scene import generate_manim_code


def main():
    print("Hello from manimator!")

def test_code_generation():
    intent = "Circle whirling sinusoidal"
    scene_plan = plan_scene(intent)
    code = generate_manim_code(scene_plan)
    print(code)


if __name__ == "__main__":
    main()
    test_code_generation()
