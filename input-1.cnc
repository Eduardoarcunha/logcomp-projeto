string sorcerer = "Daar";
string giant = "Fenir";
int sorcererLife = 5;
int giantLife = 10;

int attackRoll;
int time;

combat; time = 0; while sorcererLife > 0 && giantLife > 0 progress time = time + 1 {
    print("Current combat time: " . time . "s");
    print("");

    if (time % 2 == 0) {
        print(sorcerer . "'s turn");
        attackRoll = roll(8);
        giantLife = giantLife - attackRoll;
        print(sorcerer . " attacked " . giant . " with " . attackRoll . " points of damage!");

    } else {
        print(giant . "'s turn");
        attackRoll = roll(4);

        sorcererLife = sorcererLife - attackRoll;
        print(giant . " attacked " . sorcerer . " with " . attackRoll . " points of damage!");
    }
}
if (sorcererLife > 0) {
    print("The monster was defeated!");
} else {
    print("The player was defeated!");
}

print("Battle ended");

