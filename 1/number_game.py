import random


def number_game():
    secret_number = random.randint(1, 45)
    attempts = 0

    print("=== 숫자 맞추기 게임 ===")
    print("1부터 45 사이의 숫자를 맞춰보세요!")

    while True:
        try:
            guess = int(input("숫자를 입력하세요 (1~45): "))
        except ValueError:
            print("숫자만 입력해주세요.")
            continue

        attempts += 1

        if guess < 1 or guess > 45:
            print("범위는 1부터 45 사이여야 합니다.")
            continue

        if guess < secret_number:
            print("업! 더 큰 숫자입니다.")
        elif guess > secret_number:
            print("다운! 더 작은 숫자입니다.")
        else:
            print(f"정답입니다! {attempts}번 만에 맞추셨습니다.")
            break

    restart = input("다시 하시겠습니까? (y/n): ").strip().lower()
    if restart == "y":
        number_game()
    else:
        print("게임을 종료합니다. 수고하셨습니다!")


if __name__ == "__main__":
    number_game()
