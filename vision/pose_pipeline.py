import json
from pathlib import Path

import cv2

from .pose_detector import PoseDetector
from .landmark_extractor import LandmarkExtractor
from .landmark_visualizer import LandmarkVisualizer


class PosePipeline:

    def __init__(self):

        self.detector = PoseDetector()

        self.extractor = LandmarkExtractor()

        self.visualizer = LandmarkVisualizer()

    def process_image(
        self,
        image_path,
        annotated_output,
        json_output,
    ):

        image = cv2.imread(str(image_path))

        if image is None:

            raise FileNotFoundError(image_path)

        results = self.detector.detect(image)

        annotated = self.visualizer.draw(
            image,
            results,
        )

        landmarks = self.extractor.extract(results)

        cv2.imwrite(
            str(annotated_output),
            annotated,
        )

        with open(json_output, "w") as f:

            json.dump(
                landmarks,
                f,
                indent=4,
            )

        return annotated, landmarks