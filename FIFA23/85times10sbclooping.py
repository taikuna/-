from sbc.sbc import *

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="D:\github\video_editing_tool\Chrome automation\temp"
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9224 --user-data-dir="D:\github\video_editing_tool\Chrome automation\temp1"
port = 9222
driver = start_webdriver(port)

counter = 0
error_counter = 0
while True:
    while True:
        try:
            dub_check = Eightyfourplusten_x10_upgrade(dubs_limit=11, rating_req=88, target='86+ x10 Upgrade',
                                                      pack='85+ x10 PLAYERS PACK', driver=driver, team=team,
                                                      open_after=True, sub_target='86+ x10 Upgrade')

            counter += 1


        except Exception as e:
            print(f"An exception occurred: {str(e).split('  (Session info:')[0]}")
            error_counter += 1
            if error_counter % 3 == 0:
                driver.refresh()
                sleep(15)
            if error_counter == 12:
                send_to_telegram('エラー連発したので停止中', team)
                error_counter = 0
                print('pless "y" to continue...')
                answer = 'n'
                while True:
                    answer = input()
                    if answer == 'y':
                        break
            continue

    driver.refresh()
    sleep(20)
    # break
