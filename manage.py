from argparse import ArgumentParser
from src.make_description_images import make_description_images


if __name__ == '__main__':
    parser = ArgumentParser(description='')
    subparsers = parser.add_subparsers(help='sub-commands')
    subparsers.required = True
    subparsers.dest = 'SUB_COMMAND'

    # test project settings
    # ex: python manage.py --test-project projectX
    # ex: python manage.py -t projectX

    # make description images
    # ex: python manage.py make-image -p projectX
    # ex: python manage.py make-image --project projectX
    parser_make_each_image = subparsers.add_parser('make-image', help='make description images')
    parser_make_each_image.add_argument('-p', '--project', type=str, help='project name')
    parser_make_each_image.set_defaults(func=make_description_images)

    # concatenate description images to one image

    # make video from a concatenated image

    # convert one image to projectX.json

    # layers.jsonからsrc.structures下のクラスを自動的に構築できるようにする
    # gen / migration

    args = parser.parse_args()
    args.func(args)
