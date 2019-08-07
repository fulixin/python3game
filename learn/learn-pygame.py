import pygame
from pygame.locals import *
from sys import exit

# 窗口宽
WINDOWWIDTH = 500
# 窗口高
WINDOWHEIGHT = 376
# 窗口显示帧数(8~32)
WINDOWFRAME = 16


def main():
    # 初始化
    pygame.init()
    # 绘制窗口
    screen = pygame.display.set_mode(
        (WINDOWWIDTH, WINDOWHEIGHT), True, WINDOWFRAME)
    # 设置窗口标题
    pygame.display.set_caption('pygame测试')
    # 加载图片并转换
    background = pygame.image.load(
        r'E:/python/python3game/learn/image/sea.jpg')
    mouse_cursor = pygame.image.load(
        r'E:/python/python3game/learn/image/fish.png')

    x, y = 0, 0

    # 主循环
    while True:
        # 获取键盘点击事件
        for event in pygame.event.get():
            if event.type == QUIT:
                # 接收到退出事件后退出程序
                exit()

            # 将背景图画上去
            screen.blit(background, (0, 0))
            # # 获取鼠标位置
            # x,y=pygame.mouse.get_pos()
            # # 计算光标左上角位置
            # x-=mouse_cursor.get_width()/2
            # y-=mouse_cursor.get_height()/2

            # 获取键盘事件
            if event.type == KEYDOWN:
                # 方向键
                if event.key == K_LEFT:
                    x = x-10
                elif event.key == K_RIGHT:
                    x = x+10
                elif event.key == K_UP:
                    y = y-10
                elif event.key == K_DOWN:
                    y = y+10

            x=x+1
            y=y+1        

            if x < 0 or x > 500:
                x = 0
            if y < 0 or y > 376:
                y = 0

            # 将光标画上去
            screen.blit(mouse_cursor, (x, y))

            # 刷新画面
            pygame.display.update()


if __name__ == "__main__":
    main()
