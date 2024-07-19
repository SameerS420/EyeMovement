import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Words to display
lines = [
    ["Hello", "world", "here"],
    ["Look", "at", "me"]
]

def draw_text(frame, words, highlight_index, y):
    x0, dx = 50, 150  # Adjust dx for spacing between words
    x = x0
    for i, word in enumerate(words):
        if i == highlight_index:
            cv2.putText(frame, word, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, word, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
        x += dx

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    vertical_ratio = gaze.vertical_ratio()
    horizontal_ratio = gaze.horizontal_ratio()

    if vertical_ratio is not None and horizontal_ratio is not None:
        if vertical_ratio < 0.5:
            line_index = 0  # Look up to highlight the first line
        else:
            line_index = 1  # Look down to highlight the second line

        words = lines[line_index]
        word_index = int(horizontal_ratio * len(words))
        if word_index >= len(words):
            word_index = len(words) - 1

        for idx, line in enumerate(lines):
            if idx == line_index:
                draw_text(frame, words, word_index, 150 + idx * 100)
            else:
                draw_text(frame, line, -1, 150 + idx * 100)
    else:
        for idx, line in enumerate(lines):
            draw_text(frame, line, -1, 150 + idx * 100)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
