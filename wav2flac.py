#!/usr/bin/python3
# coding: utf-8
# 2019年11月21日作成開始
"""
フォルダ構成を維持したままWAVファイルをFLACに変換する。
完了後にWAVファイルはゴミ箱に送る。
"""
import re
import sys
from glob import glob

from send2trash import send2trash


def glob_audiofile(dir_path, audio_format):
    """
    フォルダ内の指定フォーマットの音声ファイル一覧をフルパス取得
    """
    audio_filelist = []
    # ファイルを再帰的に取得
    # 各ファイルが1KB以上であることを確認
    # 総データサイズを取得
    # ファイル一覧を返答
    return audio_filelist


def wav2flac(wav_filelist):
    """
    flac.exeを使ってWAVファイルをFLACエンコード
    この際トラック情報を取得すること
    """
    flac_exe = ''  # flac.exeのパス


def check_audiofile(wav_filelist, flac_filelist):
    """
    全てのwavファイルをflac変換できたか確認
    """
    return True


def main():
    """
    全体の処理を実行
    """
    # 処理対象フォルダを決定
    try:
        dir_path = sys.argv[1]
    except IndexError:
        dir_path = input('フォルダを指定してください\n>>> ')

    # はじめ
    print('処理を始めます。')
    print('--------------------')

    # WAVファイル一覧を取得
    wav_filelist = glob_audiofile(dir_path, 'wav')

    # WAV→FLACエンコード
    wav2flac(wav_filelist)

    # FLACファイル一覧を取得
    flac_filelist = glob_audiofile(dir_path, 'flac')

    # 正常に処理できたか確認
    if not check_audiofile(wav_filelist, flac_filelist):
        print('ファイル変換に失敗しました。')
        print('Press enter to exit.')
        sys.exit()

    # 用済みのWAVファイルをゴミ箱に送る
    for wav in wav_filelist:
        send2trash(wav)

    # おわり
    print('--------------------')
    print('処理を終えました。')
    input('Press enter to exit.')


if __name__ == '__main__':
    main()
