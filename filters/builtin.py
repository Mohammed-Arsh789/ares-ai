from __future__ import annotations

import cv2

from .base import Filter


class NoirFilter(Filter):

    name = "noir"

    def apply(self, frame):

        return cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY,
        )


class VintageFilter(Filter):

    name = "vintage"

    def apply(self, frame):

        result = frame.copy()

        result[:, :, 0] = cv2.add(
            result[:, :, 0],
            20,
        )

        return result


class SketchFilter(Filter):

    name = "sketch"

    def apply(self, frame):

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY,
        )

        inverted = cv2.bitwise_not(
            gray
        )

        blurred = cv2.GaussianBlur(
            inverted,
            (21, 21),
            0,
        )

        return cv2.divide(
            gray,
            255 - blurred,
            scale=256,
        )