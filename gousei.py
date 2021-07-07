#img_src1 入力画像1
#img_src2 入力画像2
#img_dst 合成画像

#入力画像１を濃淡画像に変換
img_g1 = cv2.cvtColor(img_src1, cv2.COLOR_BGR2GRAY)
#マスク画像生成のための２値化
img_mskg = cv2.threshold(img_g1,200,255,cv2.THRESH_BINARY_INV)[1]
#マスク画像（カラー）生成
img_msk = cv2.merge((img_mskg, img_mskg, img_mskg))
#入力画像１からマスク画像の部分だけを切り出す（切り出し画像１）
img_slm = cv2.bitwise_and(img_src1,img_msk)
#マスク画像の反転
img_mskn = cv2.bitwise_not(img_msk)
#入力画像２からマスク画像の反転部分だけを切り出す（切り出し画像２）
img_s2m = cv2.bitwise_and(imd_src2, img_mskn)
#切り出し画像１と切り出し画像２を合成
img_dst = cv2.bitwise_or(img_slm, img_s2m)
