#!/usr/bin/env python3
# coding: utf-8
# 2019年11月21日作成開始
"""
フォルダ構成を維持したままWAVファイルをFLACに変換する。
完了後にWAVファイルはゴミ箱に送る。
"""
import os
import subprocess
import sys
from glob import glob

from pydub import AudioSegment
from send2trash import send2trash
# import ffmpeg
from tqdm import tqdm

# from pysnooper import snoop


def glob_audiofile(dir_path, audio_format):
    """
    フォルダ内の指定フォーマットの音声ファイル一覧をフルパス取得
    """
    # ファイルを再帰的に取得
    audio_files = glob('{}/*.{}'.format(dir_path, audio_format))
    # ファイルサイズを取得
    audio_sizes = list(map(os.path.getsize, audio_files))
    # 総データサイズを取得
    total_size = sum(audio_sizes)
    # ファイル一覧を返答
    return audio_files, total_size


def wav2flac(wav_files):
    """
    WAVファイルをFLACエンコード
    ffmpeg.exeかflac.exeが必要
    """
    # flac.exeを利用
    if os.path.isfile('./flac.exe'):
        flac_arg = ' '.join(wav_files)
        subprocess.call('.\\flac.exe -f {}'.format(flac_arg, shell=True))  # ファイルを変換（上書き）
        subprocess.call('.\\flac.exe -t -F {}'.format(flac_arg, shell=True))  # 破損検査・修復

        # ffmpegを利用
    elif os.path.isfile('./ffmpeg.exe'):
        for wav_file in tqdm(wav_files):
            # ファイルを読み取り
            f = AudioSegment.from_file(wav_file)
            # flac用にファイル名を変更
            flac_file = wav_file.replace('.wav', '.flac')
            # flacで保存
            f.export(flac_file, format='flac')

    else:
        print('ffmpeg.exeまたはflac.exeをwavfile.pyと同じ階層に用意してください。')


def check_files(wav_files, flac_files):
    """
    全てのwavファイルをflac変換できたか確認
    """
    if len(wav_files) == len(flac_files):
        return True
    return False

# @snoop()


def main():
    """
    全体の処理を実行
    """
    # 処理対象フォルダを決定
    try:
        dir_path = sys.argv[1].replace('"', '')
    except IndexError:
        dir_path = input('フォルダを指定してください\n>>> ').replace('"', '')
    # フォルダ指定がない場合はカレントフォルダで処理
    if dir_path == (''):
        dir_path = '.'

    # はじめ
    print('処理を始めます。')
    print('--------------------')

    # WAVファイル一覧を取得
    print('WAVファイルを検索します。')
    wav_files, wav_totalsize = glob_audiofile(dir_path, 'wav')

    # WAV→FLACエンコード
    print('FLACにエンコードします。')
    wav2flac(wav_files)
    print('FLACエンコード完了しました。')

    # FLACファイル一覧を取得
    print('FLACファイルを検索します。')
    flac_files, flac_totalsize = glob_audiofile(dir_path, 'flac')

    # 正常に処理できたか確認
    print('WAVファイルとFLACファイルの個数を比較します。')
    if check_files(wav_files, flac_files):
        print('WAVファイルとFLACファイルの数が一致しました。')
        print('WAVファイルをごみ箱へ送ります。')
        # 用済みのWAVファイルをゴミ箱に送る
        for wav_file in wav_files:
            send2trash(tqdm(wav_file))
        print('WAVファイルをゴミ箱に送りました。')
    else:
        print('WAVファイルとFLACファイルの数が一致しません。')
        print('WAVファイルをごみ箱へ送るのはやめておきます。')

    # おわり
    print('--------------------')
    print('処理を終えました。')
    print('WAV ファイルの合計サイズ: {} MB'.format(wav_totalsize // 1048576))
    print('FLACファイルの合計サイズ: {} MB'.format(flac_totalsize // 1048576))
    input('Press enter to exit.')


if __name__ == '__main__':
    main()
