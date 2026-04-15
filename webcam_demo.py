import cv2
import numpy as np
import tensorflow as tf

from data.class_names import CLASS_NAMES

MODEL_PATH = "models/trained_model.h5"
CAMERA_INDEX = 0


def preprocess_frame(frame_bgr: np.ndarray) -> np.ndarray:
    """Match the deployed model input: 128x128 RGB, 0-255 (no normalization)."""
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (128, 128), interpolation=cv2.INTER_AREA)
    input_arr = tf.keras.preprocessing.image.img_to_array(frame_resized)
    return np.expand_dims(input_arr, axis=0)


def predict_top3(model, frame_bgr: np.ndarray):
    input_arr = preprocess_frame(frame_bgr)
    preds = model.predict(input_arr, verbose=0)[0]
    top3_idx = np.argsort(preds)[::-1][:3]
    return [(CLASS_NAMES[i], float(preds[i])) for i in top3_idx]


def main():
    print("Loading model from", MODEL_PATH)
    model = tf.keras.models.load_model(MODEL_PATH)

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam. Try changing CAMERA_INDEX.")

    print("\nWebcam demo started")
    print("Controls:")
    print("  P = run prediction on current frame")
    print("  ESC = exit\n")

    last_result = None

    while True:
        ok, frame = cap.read()
        if not ok:
            continue

        display = frame.copy()

        if last_result is not None:
            cv2.rectangle(display, (10, 10), (900, 120), (0, 0, 0), -1)
            for idx, (name, conf) in enumerate(last_result, start=1):
                txt = f"{idx}. {name.replace('_', ' ')} - {conf * 100:.1f}%"
                cv2.putText(
                    display,
                    txt,
                    (20, 25 + (idx * 28)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

        cv2.putText(
            display,
            "Press P to predict | ESC to exit",
            (20, display.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        cv2.imshow("KrishiMitra Webcam Demo", display)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            break
        if key in (ord("p"), ord("P")):
            last_result = predict_top3(model, frame)
            print("Top predictions:")
            for rank, (name, conf) in enumerate(last_result, start=1):
                print(f"  {rank}. {name} -> {conf * 100:.2f}%")
            print()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
