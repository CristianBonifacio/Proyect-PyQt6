import subprocess


class convert:

    def __init__(self):
        self.data = [8341260130101072, 834126013010108, 834126013010109, 834126013010110, 834126013010111, 834126013010112, 834126013010113, 834126013010114, 834126013010115]
    
    def execute(self):
        for number in self.data:

            input_file = f"D:\\audios\\Verint Original\\{number}.wav"
            output_file = f"D:\\audios\\Verint New\\{number}.wav"
            command = [
                "C:\\Program Files (x86)\\Verint\\Playback\\CommandLineConvertor.exe",
                input_file,
                output_file
            ]
            try:
                subprocess.run(command, check=True)
                print(f"Conversion successful for: {number}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting file {number}: {e}")


if __name__ == "__main__":
    convert().execute()              

