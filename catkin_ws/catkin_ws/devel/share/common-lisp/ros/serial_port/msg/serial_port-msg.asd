
(cl:in-package :asdf)

(defsystem "serial_port-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "header" :depends-on ("_package_header"))
    (:file "_package_header" :depends-on ("_package"))
    (:file "header" :depends-on ("_package_header"))
    (:file "_package_header" :depends-on ("_package"))
  ))