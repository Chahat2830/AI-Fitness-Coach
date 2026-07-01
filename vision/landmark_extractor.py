class LandmarkExtractor:

    def extract(self, results):

        if not results.pose_landmarks:
            return None

        landmarks = []

        for idx, landmark in enumerate(results.pose_landmarks.landmark):

            landmarks.append({

                "id": idx,

                "x": landmark.x,

                "y": landmark.y,

                "z": landmark.z,

                "visibility": landmark.visibility

            })

        return landmarks