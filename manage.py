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
    # ex: python manage.py make-images -p projectX
    # ex: python manage.py make-images --project projectX
    parser_make_each_image = subparsers.add_parser('make-images', help='make description images')
    parser_make_each_image.add_argument('-p', '--project', type=str, help='project name')
    parser_make_each_image.set_defaults(func=make_description_images)

    # make video from a concatenated image
    # ex: python manage.py make-video -p projectX
    # ex: python manage.py make-video --project projectX --output sample.mp4
    # parser_make_video = subparsers.add_parser('make-video', help='make video from concatenated image')
    # parser_make_video.add_argument('-p', '--project', type=str, help='project name')
    # parser_concat_images.add_argument('-o', '--output', type=str, help='output name')
    # parser_concat_images.add_argument('-t', '--output', default='mp4', type=str, help='output name')
    # parser_make_video.set_defaults(func=make_video)

    args = parser.parse_args()
    args.func(args)
