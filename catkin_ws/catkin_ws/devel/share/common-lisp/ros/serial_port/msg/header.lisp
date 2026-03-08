; Auto-generated. Do not edit!


(cl:in-package serial_port-msg)


;//! \htmlinclude header.msg.html

(cl:defclass <header> (roslisp-msg-protocol:ros-message)
  ((num1
    :reader num1
    :initarg :num1
    :type cl:fixnum
    :initform 0)
   (num2
    :reader num2
    :initarg :num2
    :type cl:fixnum
    :initform 0)
   (num3
    :reader num3
    :initarg :num3
    :type cl:fixnum
    :initform 0))
)

(cl:defclass header (<header>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <header>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'header)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name serial_port-msg:<header> is deprecated: use serial_port-msg:header instead.")))

(cl:ensure-generic-function 'num1-val :lambda-list '(m))
(cl:defmethod num1-val ((m <header>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader serial_port-msg:num1-val is deprecated.  Use serial_port-msg:num1 instead.")
  (num1 m))

(cl:ensure-generic-function 'num2-val :lambda-list '(m))
(cl:defmethod num2-val ((m <header>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader serial_port-msg:num2-val is deprecated.  Use serial_port-msg:num2 instead.")
  (num2 m))

(cl:ensure-generic-function 'num3-val :lambda-list '(m))
(cl:defmethod num3-val ((m <header>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader serial_port-msg:num3-val is deprecated.  Use serial_port-msg:num3 instead.")
  (num3 m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <header>) ostream)
  "Serializes a message object of type '<header>"
  (cl:let* ((signed (cl:slot-value msg 'num1)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'num2)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'num3)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <header>) istream)
  "Deserializes a message object of type '<header>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'num1) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'num2) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'num3) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<header>)))
  "Returns string type for a message object of type '<header>"
  "serial_port/header")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'header)))
  "Returns string type for a message object of type 'header"
  "serial_port/header")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<header>)))
  "Returns md5sum for a message object of type '<header>"
  "1e2b57837792a4e2809b7e2db06c7c3c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'header)))
  "Returns md5sum for a message object of type 'header"
  "1e2b57837792a4e2809b7e2db06c7c3c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<header>)))
  "Returns full string definition for message of type '<header>"
  (cl:format cl:nil "int16 num1~%int16 num2~%int16 num3~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'header)))
  "Returns full string definition for message of type 'header"
  (cl:format cl:nil "int16 num1~%int16 num2~%int16 num3~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <header>))
  (cl:+ 0
     2
     2
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <header>))
  "Converts a ROS message object to a list"
  (cl:list 'header
    (cl:cons ':num1 (num1 msg))
    (cl:cons ':num2 (num2 msg))
    (cl:cons ':num3 (num3 msg))
))
