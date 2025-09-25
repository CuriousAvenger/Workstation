import os
from time import time
import struct
from math import log2
from chess import pgn, Board
from io import StringIO

def get_pgn_games(pgn_string):
    games = []
    pgn_io = StringIO(pgn_string)
    while True:
        game = pgn.read_game(pgn_io)
        if game is None:
            break
        games.append(game)
    return games

def decode(pgn_string: str, output_file_path: str):
    start_time = time()
    total_move_count = 0
    games = get_pgn_games(pgn_string)
    output_data = ""

    with open(output_file_path, "wb") as output_file:
        for game_index, game in enumerate(games):
            chess_board = Board()
            game_moves = list(game.mainline_moves())
            total_move_count += len(game_moves)

            for move_index, move in enumerate(game_moves):
                legal_moves = list(chess_board.generate_legal_moves())
                legal_uci = [m.uci() for m in legal_moves]

                move_binary = bin(legal_uci.index(move.uci()))[2:]
                max_length = int(log2(len(legal_uci)))

                move_binary = move_binary.zfill(max_length)
                output_data += move_binary
                chess_board.push_uci(move.uci())

                while len(output_data) >= 8:
                    byte_chunk = output_data[:8]
                    output_file.write(struct.pack("B", int(byte_chunk, 2)))
                    output_data = output_data[8:]

        # Write remaining bits (padded) if any
        if output_data:
            output_file.write(struct.pack("B", int(output_data.ljust(8, '0'), 2)))

    print(f"[+] Decoded {len(games)} game(s) and {total_move_count} moves in {round(time() - start_time, 2)}s")
    print(f"[+] Output written to {output_file_path}")


def check_output_file(file_path):
    with open(file_path, "rb") as f:
        header = f.read(8)

    if header.startswith(b"\x89PNG"):
        print("✅ Decoded file looks like a PNG image! Rename it to decoded.png and open it.")
    elif header.startswith(b"\xFF\xD8"):
        print("✅ Decoded file looks like a JPEG image! Rename it to decoded.jpg and open it.")
    elif header.decode(errors='ignore').startswith("CTF{"):
        print("🎯 Flag detected in plain text! Open the file to view it.")
    else:
        print("ℹ️ Output does not match known file signatures. First 8 bytes:", header.hex())
        print("Try checking the file in a hex editor or an image viewer.")


def reconstruct_image_from_pgn_folder(folder_path, output_file_path):
    all_pgn_data = ""
    game_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".pgn")],
        key=lambda x: int(''.join(filter(str.isdigit, x)) or 0)
    )

    if not game_files:
        print("⚠️ No PGN files found in folder.")
        return

    for filename in game_files:
        with open(os.path.join(folder_path, filename), "r") as f:
            all_pgn_data += f.read() + "\n"

    print(f"[+] Loaded {len(game_files)} PGN files. Starting decode...")
    decode(all_pgn_data, output_file_path)
    check_output_file(output_file_path)


if __name__ == "__main__":
    input_folder = "."
    output_binary_file = "decoded_output.bin"
    reconstruct_image_from_pgn_folder(input_folder, output_binary_file)
