from .schemas import ScenePlan, ObjectPlan, MotionPlan

def plan_scene(intent: str) -> ScenePlan:
    if "circle whirling sinusoidal" in intent.lower():
        obj = ObjectPlan(id="circle1", type="circle", radius=0.4)
        motions = [
            MotionPlan(target="circle1", motion="sinusoidal_path", params={"amplitude": 2, "frequency": 1}),
            MotionPlan(target="circle1", motion="rotation", params={"angular_speed": 4}),
        ]
        return ScenePlan(objects=[obj], motions=motions, duration=6)
    
    return ScenePlan(objects=[], motions=[], duration=5)
