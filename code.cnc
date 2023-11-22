action sub(a int, b int) int {
    act a - b;
}

string sorcerer = "Daar";
string cleric = "Reegull";
string giant = "Fenir";

int sorcererLife = 10;
int clericLife = 10;
int giantLife = 20;

int sorcererDice = 10;
int clericDice = 6;
int giantDice = 4;

int attackRoll;
int time;

combat; time = 0; while (sorcererLife > 0 || clericLife > 0) && giantLife > 0 progress time = time + 1 {
    print("Current combat time: " . time . "s");
    print("");

    if (time % 3 == 0) {
        print(sorcerer . "'s turn");
        attackRoll = roll(sorcererDice);
        giantLife = sub(giantLife, attackRoll);
        print(sorcerer . " attacked " . giant . " with " . attackRoll . " points of damage!");

    } else {
        if (time % 3 == 1) {
            print(cleric . "'s turn");
            attackRoll = roll(clericDice);
            giantLife = sub(giantLife, attackRoll);
            print(cleric . " attacked " . giant . " with " . attackRoll . " points of damage!");

        } else {
            print(giant . "'s turn");
            attackRoll = roll(giantDice);

            if (roll(2) == 1) {
                sorcererLife = sub(sorcererLife, attackRoll);
                print(giant . " attacked " . sorcerer . " with " . attackRoll . " points of damage!");

            } else {
                clericLife = sub(clericLife, attackRoll);
                print(giant . " attacked " . cleric . " with " . attackRoll . " points of damage!");
            }
        }
    }
}

if (sorcererLife > 0 || clericLife > 0) {
    print("The monster was defeated!");
} else {
    print("The players were defeated!");
}

print("Battle ended");

