import cv2
import numpy as np
triangle_template = cv2.imread('triangle_image.png', cv2.IMREAD_GRAYSCALE)
triangle_height, triangle_width = triangle_template.shape[:2]
test_image_path = 'test_image.png'
target_image_path = 'target_image3.png'
def detect_and_display():
    test_image = cv2.imread(test_image_path)
    test_image_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    result_triangle = cv2.matchTemplate(test_image_gray, triangle_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_triangle)
    if max_val >= 0.8:
        triangle_top_left = max_loc
        triangle_bottom_right = (triangle_top_left[0] + triangle_width, triangle_top_left[1] + triangle_height)
        top_offset = 150
        bottom_offset = 233
        region_top_left = (triangle_top_left[0], triangle_top_left[1] - top_offset)
        region_bottom_right = (triangle_top_left[0] + triangle_width + bottom_offset, triangle_top_left[1])
        region = test_image[region_top_left[1]:region_bottom_right[1], region_top_left[0]:region_bottom_right[0]]
        region_gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(region_gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        min_contour_area = 58
        max_contour_area = 70
        filtered_image = np.zeros_like(edges)
        for contour in contours:
            contour_area = cv2.contourArea(contour)
            if min_contour_area < contour_area < max_contour_area:
                cv2.drawContours(filtered_image, [contour], -1, (255), thickness=cv2.FILLED)
        target_template = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
        target_height, target_width = target_template.shape[:2]
        result_target = cv2.matchTemplate(filtered_image, target_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_target)
        threshold = 0.8
        if max_val >= threshold:
            target_top_left = max_loc
            target_bottom_right = (target_top_left[0] + target_width, target_top_left[1] + target_height)
            cv2.rectangle(filtered_image, target_top_left, target_bottom_right, (0, 0, 255), 2)
            filter_colored = cv2.cvtColor(filtered_image, cv2.COLOR_GRAY2BGR)
            filter_colored = cv2.rectangle(filter_colored, target_top_left, target_bottom_right, (0, 0, 255), 2)
            cv2.imshow('Filtered Image with Target Detection', filter_colored)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Target image not found.")
detect_and_display()

 # algılanan puzzleın kenarlıklarını kontürle cizer, cizilen konturlerin uzerinde image recognition atar