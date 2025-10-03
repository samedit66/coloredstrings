from yachalk import chalk
from coloredstrings import style

s1 = chalk.italic
s2 = s1.red

print(s1("Chalk, am I red?"))
print(s2("Yes, you are!"))

print("-" * 8)

s3 = style.italic
s4 = s3.red

print(s3("Style, am I still red?"))
print(s4("Sure not, but I am!"))
