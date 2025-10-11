from yachalk import chalk

import coloredstrings as cs

# With yachalk
s1 = chalk.italic
s2 = s1.red

print(s1("Chalk, am I red?"))
print(s2("Yes, you are!"))

print("-" * 8)

# With coloredstrings
s3 = cs.italic
s4 = s3.red

print(s3("Style, am I still red?"))
print(s4("Sure not, but I am!"))
