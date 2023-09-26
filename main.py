from pyuac import main_requires_admin
from vision_code import vision


@main_requires_admin
def main():
    vision()

if __name__ == "__main__":
    main()