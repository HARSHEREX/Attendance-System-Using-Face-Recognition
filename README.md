# Attendance System Using Face Recognition.




## Please Note:
- While adding the student there should be enough light arround the person's face

Initial Step:
	--Install python 3
	--Open cmd/terminal
	--Type pip
		If No error then proceed to next steps

Intermediate Steps:
	--open cmd/terminal
	Type the following commands one by one

		pip install opencv-python
		pip install pytest-shutil
		pip install pandas
		pip install tkintertable
		pip install tk-tools
		pip install pyttk
		pip install Pillow==2.2.1
		pip install numpy
		pip install python-csv
		pip install opencv_contrib_python

## Final Steps:
	
Run the "Run.cmd" file 

If any module import error occurs please install the mudule by the module name

## How To Use:
	The UI is very simple and there is validation at every step, for better user experience
	you can directly use the software to understand its working

- Or follow these instructions:

	- After running "Run.cmd" file. 
	- A Window will start which is basically a form. 
	- Enter integer id of the student.
	- Enter name of the student. 
	- Press "Add Student" button (NOTE:- User can as many students as user want, they will be saved to "DATA\Registration\StudentDetails.csv")
	- If re-registation is needed then first delete the student record using entering the id of the student and then press remove button 
	- (NOTE:-User can delete as many student as user want).
	- After deletion Model Training is necessary.
	- After successful registration press "Train Model" button to train the model.
	- To take attendance press "Take Attendance" button.
	- The attendance will be saved to dir:("DATA\Attendance\") in a .csv file with date and time. 












	
	



