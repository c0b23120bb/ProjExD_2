import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pg_move = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (5,0)
}  #移動用辞書の設定



def check_bound(obj_rct):  #画面外、画面内の判定
    horizontal, vertical = True, True  #横、縦が画面内

    if obj_rct.left < 0 or WIDTH < obj_rct.right:  #左右の画面外
        horizontal = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:  #上下の画面外
        vertical = False
    
    return horizontal, vertical



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    bd_img = pg.Surface((20, 20))  #爆弾の作成
    bd_img.set_colorkey((0,0,0))  #黒の枠を無くす
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)  #円、赤、半径10
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  #ランダムに生成
    vx, vy = +5, +5

    #ゲームオーバー画面
    gm_img = pg.Surface((WIDTH,HEIGHT))  #ブラックアウト
    pg.draw.rect(gm_img,(0),(0,0,WIDTH,HEIGHT))
    gm_img.set_alpha(150) #半透明
    gm_rct = gm_img.get_rect()
    gm_rct.center = WIDTH/2, HEIGHT/2
    fonto = pg.font.Font(None,100) 
    txt = fonto.render("Game Over",True,(0))

    gm_kk_img = pg.transform.rotozoom(pg.image.load("fig/2.png"), 0, 2.0)
    gm_kk_img2 = pg.transform.flip(gm_kk_img,True,False) #画像反転
    

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct): #こうかとんと爆弾の衝突時
            print("GameOver")

            #ブラックアウトと文字、こうかとんの表示
            screen.blit(gm_img,gm_rct)
            screen.blit(txt,[WIDTH/2 - 170, HEIGHT/2 - 40])
            screen.blit(gm_kk_img, (500,370))
            screen.blit(gm_kk_img2, (1050,370))
            
            pg.display.update()
            pg.time.wait(5000)  #5秒間止める
            return #mainから抜ける

        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k,v in pg_move.items():
            if key_lst[k]:  #対応するキーが押されていたら
                sum_mv[0] += v[0]  #上下
                sum_mv[1] += v[1]  #左右

        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #   sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #   sum_mv[0] += 5

        kk_rct.move_ip(sum_mv)
        bd_rct.move_ip(vx, vy)  #爆弾移動

        if check_bound(kk_rct) != (True, True):  #画面外でそれ以上進まない
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        horizontal, vertical = check_bound(bd_rct)  #爆弾の跳ね返り
        if horizontal != True:
            vx *= -1  #反転
        if vertical != True:
            vy *= -1

        screen.blit(kk_img, kk_rct)
        screen.blit(bd_img, bd_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
