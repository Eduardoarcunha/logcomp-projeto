action rollAndAttack(diceSides int, attackedEnemy string, attackedEnemyHealth int) int {
    int damage = roll(diceSides);
    print(attackedEnemy . " got hit! Damage dealt: " . damage);

    act attackedEnemyHealth - damage;
}

string knight = "Charles";
string enemy = "Dragon";
int enemyHealth = 10;

enemyHealth = rollAndAttack(10, enemy, enemyHealth);
print("Enemy is now at: " . enemyHealth . " life!");
