import Square from "./Square";

type ChessBoardProps = {
    chessColourWhite: string;
    chessColourBlack: string;
    gridColumn: number
};


function ChessBoard({chessColourWhite, chessColourBlack, gridColumn }: ChessBoardProps) {

    return (
        <div
            className="chess-board"
            style={{
                gridColumn: gridColumn,
                minWidth: 0,
            }}
        >
            {Array.from({ length: 8 }, (_, row) =>
                Array.from({ length: 8 }, (_, col) => (
                    <Square
                        key={`${row}-${col}`}
                        id={`${row}-${col}`}
                        x={col * 12.5}
                        y={row * 12.5}
                        colour={
                            (row + col) % 2 === 0
                                ? chessColourWhite
                                : chessColourBlack
                        }
                    />
                ))
            )}
        </div>
    );



}

export default ChessBoard;