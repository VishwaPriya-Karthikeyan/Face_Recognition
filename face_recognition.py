from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from time import strftime
from datetime import datetime
import cv2
import os
import numpy as np

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 35, "bold"), bg="white", fg="green")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # 1st button
        img_top = Image.open(r"C:\Users\muthu\Desktop\Face Recognition\college_images\dect.jpg")
        img_top = img_top.resize((650, 700), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=650, height=700)

        # 2nd button
        img_bottom = Image.open(r"C:\Users\muthu\Desktop\Face Recognition\college_images\dect2.jpg")
        img_bottom = img_bottom.resize((950, 700), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl = Label(self.root, image=self.photoimg_bottom)
        f_lbl.place(x=650, y=55, width=950, height=700)

        # Button
        b1_1 = Button(f_lbl, text="Face Recognition", cursor="hand2", command=self.face_recog, font=("times new roman", 18, "bold"), bg="darkgreen", fg="white")
        b1_1.place(x=365, y=620, width=200, height=40)

        # Binding window close event to properly release camera
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Handler to properly close the window and release the camera."""
        print("Window closed. Releasing camera...")
        if hasattr(self, 'video_cap'):
            self.video_cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

    # ===================== Attendance ============================
    def mark_attendance(self, i, r, n, d):
        with open("vishwa.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()
            name_list = []
            for line in myDataList:
                entry = line.split(",")  # Fixed incorrect comparison operator
                name_list.append(entry[0])

            if (i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list):
                now = datetime.now()
                d1 = now.strftime("%d/%m/%y")
                dtString = now.strftime("%H:%M:%S")
                f.write(f"\n{i},{r},{n},{d},{dtString},{d1},Present")  # Fixed file writing error

    # ====================== Face Recognition ========================
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            coord = []

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                conn = mysql.connector.connect(host="localhost", username="root", password="Vishwa@3027", database="face_recognizer")
                my_cursor = conn.cursor()

                # Fetch student data safely
                def fetch_value(query):
                    my_cursor.execute(query)
                    result = my_cursor.fetchone()
                    return "+".join(result) if result else "Unknown"

                i = fetch_value(f"SELECT Student_id FROM student WHERE Student_id={id}")
                n = fetch_value(f"SELECT Name FROM student WHERE Student_id={id}")
                r = fetch_value(f"SELECT Roll FROM student WHERE Student_id={id}")
                d = fetch_value(f"SELECT Dep FROM student WHERE Student_id={id}")

                if confidence > 77:
                    cv2.putText(img, f"ID:{i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Roll:{r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name:{n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Department:{d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    self.mark_attendance(i, r, n, d)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                coord = [x, y, w, h]

            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        self.video_cap = cv2.VideoCapture(0)  # Store the capture object as a class variable

        while True:
            ret, img = self.video_cap.read()
            if not ret:
                print("Error: Failed to capture image.")
                break
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Welcome To Face Recognition", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
                print("Exiting...")
                break

        self.video_cap.release()  # Release the capture here as well, in case the user closes the window first
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()