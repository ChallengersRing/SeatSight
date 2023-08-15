import torch
import cv2
from .tools import get_logger

class Detector:
    def __init__(self, yolo_path, model_path, names_path):
        """
        Initializes the Detector class.
        Load the Model
        Args:
            yolo_path (str): Path to the YOLO model.
            model_path (str): Path to the YOLO model weights.
            names_path (str): Path to the file containing class names.
        """
        self.__model = torch.hub.load(yolo_path, 'custom', path=model_path, source='local',force_reload=True)
        with open(names_path, "r") as f:
            self.__classes = [line.strip() for line in f.readlines()]

    # Public API
    def predict(self, frame, iou_threshold=0.5):
        """
        Predicts chair occupancy in a given frame.

        Args:
            frame (numpy.ndarray): The input image frame.
            iou_threshold (float, optional): IoU threshold for occupancy check. Default is 0.5.
            height_alignment_threshold (float, optional): Height alignment threshold for chair and person. Default is 0.1.
            vertical_range (int, optional): Vertical range for chair and person alignment. Default is 50.

        Returns:
            numpy.ndarray: The input frame with bounding boxes drawn.
            list: List containing information about detected objects.
        """
        logger = get_logger()
        results = self.__model(frame)
        
        chair_boxes, chair_confidences, person_boxes, person_confidences, classes_detected = self.__filter_result(results)
        logger.info(f'Chairs({len(chair_boxes)}) : {chair_boxes} {chair_confidences}')
        logger.info(f'Persons({len(person_boxes)}) : {person_boxes} {person_confidences}')
        # for chair in chair_boxes:
        #     self.__draw_bounding_boxes(frame, chair, chair[0], "chair", (245,245,114))
        for person in person_boxes:
            self.__draw_bounding_boxes(frame, person, person[0], "human", (6, 85, 63))
        
        chair_indices = self.__perform_NMS(chair_boxes, chair_confidences, 0.5, 0.5)
        logger.info(f'chair indices : {chair_indices}')
        
        occupied_chairs_boxes, occupied_chairs_confidences, vacant_chairs_boxes, vacant_chairs_confidences = self.__find_occupied_and_vacant_chairs(frame, chair_indices, chair_boxes, chair_confidences, person_boxes, iou_threshold)
        logger.info(f'occupied chairs({len(occupied_chairs_boxes)}) : {occupied_chairs_boxes} {occupied_chairs_confidences}')
        logger.info(f'vacant chairs({len(vacant_chairs_boxes)}) : {vacant_chairs_boxes} {vacant_chairs_confidences} \n\n')
        
        data = [classes_detected, len(chair_boxes), len(person_boxes), len(occupied_chairs_boxes), len(vacant_chairs_boxes)]
        return frame, data
    
    # Internal API's
    def __filter_result(self, results):
        chair_boxes = []
        chair_confidences = []
        person_boxes = []
        person_confidences=[]
        classes_detected = []
        # iterating predictions
        for det in results.xyxy[0]:
            # [x_min, y_min, x_max, y_max, confidence, class_prediction]
            confidence = det[4].item()
            predicted_class_id = int(det[5].item())
            class_name = self.__classes[predicted_class_id]
            classes_detected.append(f'{class_name} {confidence:.2f}')
            if confidence > 0.5 and (class_name == "chair" or class_name == "person"):
                x1, y1, x2, y2 = det[:4].tolist()
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                if  class_name == "chair":
                    chair_boxes.append([x1, y1, x2, y2])
                    chair_confidences.append(float(confidence))
                elif class_name == "person":
                    person_boxes.append([x1, y1, x2, y2])
                    person_confidences.append(float(confidence))
        return chair_boxes, chair_confidences, person_boxes, person_confidences, classes_detected 
    
    def __perform_NMS(self, boxes, confidences, score, nms):
        """
        Perform non-maximum suppression on the chair boxes
        This line of code is using the OpenCV NMSBoxes function to apply Non-Maximum Suppression (NMS) on the detected chair bounding boxes. NMSBoxes takes the following arguments:
        boxes: A list of bounding boxes.
        confidences: A list of confidence scores for each bounding box.
        score_threshold: A threshold value for confidence scores. Boxes with scores below this threshold are filtered out.
        nms_threshold: A threshold value for IoU (Intersection over Union) between two boxes. Boxes with an IoU value greater than or equal to this threshold are considered redundant and only the one with the highest confidence score is kept.
        The function returns the indices of the remaining boxes after NMS is applied. These indices can be used to filter out the boxes and confidence scores that were suppressed by NMS.
        """
        return cv2.dnn.NMSBoxes(boxes, confidences, score, nms)

    def __find_occupied_and_vacant_chairs(self, frame, chair_indices, chair_boxes, chair_confidences, person_boxes, iou_threshold):
        occupied_chairs_boxes = []
        occupied_chairs_confidences = []
        vacant_chairs_boxes = []
        vacant_chairs_confidences = []
        
        for i in chair_indices:
            chair_box = chair_boxes[i]
            chair_confidence = chair_confidences[i]
            is_vacant = self.__check_vacant_chair(chair_box, person_boxes, iou_threshold)
            
            if is_vacant:
                vacant_chairs_boxes.append(chair_box)
                vacant_chairs_confidences.append(chair_confidence)
                self.__draw_bounding_boxes(frame, chair_box, chair_confidence, "Vacant", (50,205,50))
            else:
                occupied_chairs_boxes.append(chair_box)
                occupied_chairs_confidences.append(chair_confidence)
                self.__draw_bounding_boxes(frame, chair_box, chair_confidence, "Occupied", (250,128,114))
                
        return occupied_chairs_boxes, occupied_chairs_confidences, vacant_chairs_boxes, vacant_chairs_confidences
    
    def __check_vacant_chair(self, chair_box, person_boxes, iou_threshold):
        for person_box in person_boxes:
            iou = self.__calculate_iou(person_box, chair_box)
            if iou > iou_threshold:
                return False
        return True
    
    # def __check_vacant_chair(self, chair_box, person_boxes, iou_threshold, height_alignment_threshold=0.1, vertical_range=50):
    #     chair_height = chair_box[3] - chair_box[1]
    #     for person_box in person_boxes:
    #         iou = self.__calculate_iou(person_box, chair_box)
    #         if iou > iou_threshold:
    #             person_height = person_box[3] - person_box[1]
    #             height_diff = abs(chair_height - person_height)
    #             if height_diff <= height_alignment_threshold and person_box[1] - chair_box[1] <= vertical_range:
    #                 return False
    #     return True
    
    def __calculate_iou(self, person_box, chair_box):
        # Compute the coordinates of the intersection and union rectangles
        intersection_x1 = max(person_box[0], chair_box[0])
        intersection_y1 = max(person_box[1], chair_box[1])
        intersection_x2 = min(person_box[2], chair_box[2])
        intersection_y2 = min(person_box[3], chair_box[3])
        intersection_area = max(0, intersection_x2 - intersection_x1 + 1) * max(0, intersection_y2 - intersection_y1 + 1)
        union_area = (person_box[2] - person_box[0] + 1) * (person_box[3] - person_box[1] + 1) + (chair_box[2] - chair_box[0] + 1) * (chair_box[3] - chair_box[1] + 1) - intersection_area
        # Compute the IoU score between the person and chair boxes
        return intersection_area / union_area
    
    def __draw_bounding_boxes(self, frame, box, confidence, cls, color):
        x1, y1, x2, y2 = box
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        text_size = cv2.getTextSize(f'{cls} {confidence:.2f}', cv2.FONT_HERSHEY_PLAIN, 1, 2)[0]
        cv2.rectangle(frame, (x1, y1), (x1 + max(text_size[0], x2 - x1), y1 + 20), color, -1)
        cv2.putText(frame, f'{cls} {confidence:.2f}', (x1, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2)