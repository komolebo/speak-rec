train:
		sudo python speaker-recognition.py -t enroll -i "bob/ mary/ person*" -m model.out

predict:
		sudo python speaker-recognition.py -t predict -i "*.wav" -m model.out

all: train predict
