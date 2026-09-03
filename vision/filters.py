from pathlib import Path

import cv2


class ImageFilters:
    @staticmethod
    def grayscale(
        input_path,
        output_path="data/filter_grayscale.jpg",
    ):
        image = cv2.imread(
            str(input_path)
        )

        if image is None:
            raise ValueError(
                "Could not read image."
            )

        result = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cv2.imwrite(
            str(output_path),
            result,
        )

        return str(output_path)

    @staticmethod
    def edge(
        input_path,
        output_path="data/filter_edges.jpg",
    ):
        image = cv2.imread(
            str(input_path)
        )

        if image is None:
            raise ValueError(
                "Could not read image."
            )

        result = cv2.Canny(
            image,
            100,
            200,
        )

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cv2.imwrite(
            str(output_path),
            result,
        )

        return str(output_path)