;; Auto-generated. Do not edit!


(when (boundp 'serial_port::header)
  (if (not (find-package "SERIAL_PORT"))
    (make-package "SERIAL_PORT"))
  (shadow 'header (find-package "SERIAL_PORT")))
(unless (find-package "SERIAL_PORT::HEADER")
  (make-package "SERIAL_PORT::HEADER"))

(in-package "ROS")
;;//! \htmlinclude header.msg.html


(defclass serial_port::header
  :super ros::object
  :slots (_num1 _num2 _num3 ))

(defmethod serial_port::header
  (:init
   (&key
    ((:num1 __num1) 0)
    ((:num2 __num2) 0)
    ((:num3 __num3) 0)
    )
   (send-super :init)
   (setq _num1 (round __num1))
   (setq _num2 (round __num2))
   (setq _num3 (round __num3))
   self)
  (:num1
   (&optional __num1)
   (if __num1 (setq _num1 __num1)) _num1)
  (:num2
   (&optional __num2)
   (if __num2 (setq _num2 __num2)) _num2)
  (:num3
   (&optional __num3)
   (if __num3 (setq _num3 __num3)) _num3)
  (:serialization-length
   ()
   (+
    ;; int16 _num1
    2
    ;; int16 _num2
    2
    ;; int16 _num3
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int16 _num1
       (write-word _num1 s)
     ;; int16 _num2
       (write-word _num2 s)
     ;; int16 _num3
       (write-word _num3 s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int16 _num1
     (setq _num1 (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _num2
     (setq _num2 (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _num3
     (setq _num3 (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get serial_port::header :md5sum-) "1e2b57837792a4e2809b7e2db06c7c3c")
(setf (get serial_port::header :datatype-) "serial_port/header")
(setf (get serial_port::header :definition-)
      "int16 num1
int16 num2
int16 num3
")



(provide :serial_port/header "1e2b57837792a4e2809b7e2db06c7c3c")


