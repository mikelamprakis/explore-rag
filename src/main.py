from src.crew import DebateApp


def run():
    inputs = {
        'motion' : 'The round pizza is better that square pizza',
    }

    try:
        result = DebateApp().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f'An error occurred while running the crew: {e}')


if __name__ == '__main__':
    run()