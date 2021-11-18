import requests


def shuffle(x):
    """
        Shuffles a list of numbers from start to end.
    """

    try:
        api_url = "http://www.random.org/integers/?num={num}&min={start}&max={end}&col=1&base=10&format=plain&rnd=new"
        api_url = api_url.format(num=len(x), start=0, end=len(x) - 1)

        response = requests.get(api_url)
        response.raise_for_status()
        new_order = response.text.splitlines()

        return [x[int(i)] for i in new_order]

    except requests.exceptions.HTTPError:
        return x