import Square from "./Square";

type ChessBoardProps = {
    x: number;
    y: number;
    size: number;
    chessColourWhite: string;
    chessColourBlack: string;
};


function ChessBoard({ x, y, size, chessColourWhite, chessColourBlack }: ChessBoardProps) {
    return (
        <div
            className="chess-board"
            style={{
                left: `${x}vw`,
                top: `${y}vh`,
                width: `${size}vmin`,
                height: `${size}vmin`,
            }}
        >
            {Array.from({ length: 8 }, (_, row) =>
                Array.from({ length: 8 }, (_, col) => (
                    <Square
                        key={`${row}-${col}`}
                        id={`${row}-${col}`}
                        x={col * 12.5}
                        y={row * 12.5}
                        colour={(row + col) % 2 === 0
                            ? chessColourWhite
                            : chessColourBlack}
                    />
                ))
            )}
        </div>
    );
}

export default ChessBoard;