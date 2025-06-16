from app.data.ml.material_detector import MaterialDetector

class ClasificarMaterialesUseCase:
    def __init__(self, detector: MaterialDetector):
        self.detector = detector

    def execute(self, image_path: str):
        return self.detector.predict(image_path)
