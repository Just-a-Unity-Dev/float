![float, the dice, laying on a desk with battlemaps and folder](./.github/banner.png)

# float

a simple dice roller bot made for me and my friends. hosted under MIT license.

mostly on maintenance because there's not much stuff you can put in a diceroller bot.

[support me on ko-fi](https://ko-fi.com/raincaldwell)

## how do i host this

float has only been tested on docker. podman may be broken, refer to [this issue for more](https://github.com/Just-a-Unity-Dev/float/issues/1).

### docker

1. install `docker`, `docker-compose` and git by extension
2. clone this repo with git
3. checkout the version that suits your need
4. `docker-compose build`
5. `docker run -e TOKEN=<DISCORD_TOKEN> -d float_bot`
6. `history -c` to clear your history so that the token is hidden

### podman

1. install `podman` and relevant
2. clone this repo with git
3. checkout the version that suits your need
4. `podman build .`
5. get image id in `podman images`
6. `podman run -e TOKEN=<DISCORD_TOKEN> -d <IMAGE_ID>`
7. `history -c` to clear your history so that the token is hidden
