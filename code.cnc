action soma(a int, b int) int{
    act a + b;
}

string hero = input();
string enemy = input();


int hero_health = 100;
int enemy_health = 80;
int time = 0;

print("Battle begins");

combat ; time = 0 ;  while hero_health > 0 && enemy_health > 0 progress time = time + 1 {
    enemy_health = enemy_health - 10;
    print("Hero attacks!");
    print(enemy_health);
    hero_health = hero_health - 5;
    print("Enemy counterattacks!");
    print(hero_health);
}

if hero_health > 0 {
    print("Hero wins!");
} else {
    print("Enemy wins!");
}

print("Remaining health:");
print(soma(hero_health, enemy_health));