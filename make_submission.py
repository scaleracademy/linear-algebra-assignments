import os
import shutil


def make_submission():
    from solutions.student_details import scaler_email
    scaler_email = scaler_email.split('@')[0]
    # remove any files mentioned in the .gitignore file using git clean -fX
    os.system('git clean -fqdX solutions/')
    # create the zip file from the 'solutions' directory
    output_filename = f'solutions_{scaler_email}'
    shutil.make_archive(output_filename, 'zip', '.', 'solutions')
    print('\n\n\n' + '=' * 100)
    print('Submission file created:', '\u001b[42m\u001B[30m', f'solutions_{scaler_email}.zip', '\033[0m', '\nupload it to the dashboard')
    print('=' * 100)


def run():
    try:
        from solutions.pldu import pldu
        from solutions.equations import solve, det
        from solutions.simplex import simplex
        from solutions import student_details
        from solutions.student_details import scaler_email, name

        assert scaler_email.strip() != '', 'Please enter your email id in solutions/student_details.py'
        assert name.strip() != '', 'Please enter your name in solutions/student_details.py'
    except ImportError:
        print('\n\u001b[41m\u001B[30m',
              'incorrect directory structure - please follow the instructions provided in README.md')
    except AssertionError as e:
        print('\n\u001b[41m\u001B[30m', e)
        return

    import checker

    checker.check_all()

    make_submission()
    print('\033[0m')


if __name__ == '__main__':
    run()
