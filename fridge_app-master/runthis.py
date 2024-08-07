import multiprocessing
import subprocess

def run_script(script_name):
    try:
        subprocess.run(['python', script_name])
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_script, args=('qrbot.py',))
    p2 = multiprocessing.Process(target=run_script, args=('app.py',))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("SUCCESS")
