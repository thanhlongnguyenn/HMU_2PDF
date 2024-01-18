import os
import requests
from PIL import Image
from gooey import Gooey, GooeyParser, local_resource_path
import shutil

PROGRAM_NAME = "HMU_2PDF"


@Gooey(program_name=PROGRAM_NAME,
       image_dir=local_resource_path('logo'))
def main():
    parser = GooeyParser(description="PDF Downloader from HMU Online Library by @thanhlong.___ ")

    parser.add_argument("startpage", metavar="Start Page", action="store", help="First page of PDF file", type=int)
    parser.add_argument("endpage", metavar="End Page", action="store", help="Last page of PDF file", type=int)
    parser.add_argument("URL", metavar="URL", action="store", help="Documents\' URL (Log in required)")
    parser.add_argument("finaldestination", metavar="Final Destination", widget="FileSaver",
                        help="Location of saved PDF", gooey_options={
                            'wildcard': "PDF (*.pdf)|*.pdf|",
                            'message': "Location of PDF file"})

    args = parser.parse_args()

    def get_url(linkSach):
        a = linkSach.replace("FullBookReader.aspx?Url=/pages/cms/", "")
        return a[:-49]

    returnUrl = get_url(args.URL)

    def download_images(start, end):
        if not os.path.exists('imgs'):
            os.makedirs('imgs')

        # with tqdm(range(start, end+1)) as t:
        for i in range(start, end + 1):
            generated_url = (returnUrl + f'FullPreview/{str(i).zfill(6)}.jpg')
            response = requests.get(generated_url)
            if response.status_code == 200:
                with open(f'imgs/{str(i).zfill(6)}.jpg', 'wb') as handle:
                    response = requests.get(generated_url, stream=True)
                    handle.write(response.content)

            # print(f"URL: {generated_url}, status code: {response.status_code}") 
            # debugging line

    def convert_imgs_folder_to_pdf(start, end, destination):
        img_list = []

        for i in (range(start, end + 1)):
            with Image.open(f'imgs/{str(i).zfill(6)}.jpg') as image:
                img_list.append(image.convert('RGB'))

        img_list[0].save(f'{destination}', save_all=True, append_images=img_list[1:])
        print(f'The pdf is saved at: .{destination}. \nChúc bạn học tốt!')

        # auto open result pdf
        os.system(f'open {destination}')

    download_images(int(args.startpage), int(args.endpage))
    convert_imgs_folder_to_pdf(int(args.startpage), int(args.endpage), args.finaldestination)

    # Clean ./imgs folder after converting to pdfs
    shutil.rmtree('./imgs')


main()
