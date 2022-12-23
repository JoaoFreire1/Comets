# Comets
## Autoria
Rodrigo Pires 22103008 / João Freire 22104799
## Work report
Base line code - João Freire
Bug fixes - João Freire / Rodrigo Pires
Extra features missing from base line - Rodrigo Pires
Assets - João Freire
Markdown - Rodrigo Pires
## Repositório
https://github.com/JoaoFreire1/Comets.git

## Arquitetura da solução
We have `Player`, `Bullets` and `Asteroid` as the main pieces of this project. All 3 are classes with their own move and capability to verify if they are out of of the screen or not.
`Player` is composed of it's sprite, position (x,y), height and width, head and angle.
`Bullets` is composed of it's position (x,y), height and width.
`Asteroid` is composed of it's sprite, position (x,y), height and width and rank.
Both the `Player` and `Asteroid` have the capability of not leaving the boundaries of the screen by teleporting to the other side of the screen or by destruction upon entering the outside, respectively.

