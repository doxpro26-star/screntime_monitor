"""
Object detection module using YOLOv8 for phone and laptop detection.
Optimized for real-time performance.
"""

import torch
from ultralytics import YOLO
import cv2
import numpy as np
from typing import Dict, List, Tuple


class DeviceDetector:
    """Optimized device detector using YOLOv8."""
    
    def __init__(self, config: Dict):
        """
        Initialize the detector with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.confidence_threshold = config['detection']['confidence_threshold']
        self.target_classes = config['detection']['target_classes']
        
        # Initialize model
        model_name = config['detection']['model']
        device = config['detection']['device']
        
        print(f"Loading model: {model_name} on {device}...")
        self.model = YOLO(model_name)
        
        # Move to GPU if available and configured
        if device == "cuda" and torch.cuda.is_available():
            self.model.to('cuda')
            print("Using GPU acceleration")
        else:
            print("Using CPU")
        
        # Warm up model with dummy inference
        dummy_img = np.zeros((640, 640, 3), dtype=np.uint8)
        _ = self.model(dummy_img, verbose=False)
        print("Detector ready!")
    
    def detect(self, frame: np.ndarray) -> Dict[str, List[Tuple]]:
        """
        Detect devices in frame.
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Dictionary with 'phone' and 'laptop' keys containing lists of bounding boxes
        """
        results = self.model(frame, verbose=False, conf=self.confidence_threshold)[0]
        
        detections = {
            'phone': [],
            'laptop': []
        }
        
        # Extract detections
        if results.boxes is not None:
            boxes = results.boxes.xyxy.cpu().numpy()  # Bounding boxes
            confidences = results.boxes.conf.cpu().numpy()  # Confidence scores
            classes = results.boxes.cls.cpu().numpy()  # Class IDs
            
            for box, conf, cls in zip(boxes, confidences, classes):
                cls_id = int(cls)
                
                # Check if it's a phone
                if cls_id == self.target_classes['phone']:
                    detections['phone'].append({
                        'bbox': box,
                        'confidence': float(conf)
                    })
                
                # Check if it's a laptop
                elif cls_id == self.target_classes['laptop']:
                    detections['laptop'].append({
                        'bbox': box,
                        'confidence': float(conf)
                    })
        
        return detections
    
    def draw_detections(self, frame: np.ndarray, detections: Dict) -> np.ndarray:
        """
        Draw bounding boxes and labels on frame.
        
        Args:
            frame: Input frame
            detections: Detection results from detect()
            
        Returns:
            Frame with drawn detections
        """
        annotated_frame = frame.copy()
        
        # Define colors (BGR format)
        colors = {
            'phone': (0, 255, 0),    # Green
            'laptop': (255, 0, 0)     # Blue
        }
        
        for device_type, device_list in detections.items():
            color = colors.get(device_type, (255, 255, 255))
            
            for detection in device_list:
                bbox = detection['bbox']
                conf = detection['confidence']
                
                # Draw bounding box
                x1, y1, x2, y2 = map(int, bbox)
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                label = f"{device_type.capitalize()}: {conf:.2f}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                
                # Background for text
                cv2.rectangle(
                    annotated_frame,
                    (x1, y1 - label_size[1] - 10),
                    (x1 + label_size[0], y1),
                    color,
                    -1
                )
                
                # Text
                cv2.putText(
                    annotated_frame,
                    label,
                    (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1
                )
        
        return annotated_frame
