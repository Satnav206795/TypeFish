type ChessPieceProps = {
    image : string
}

function ChessPiece({image}: ChessPieceProps) {
    return (
        <img
        src={image}
        className="chess-piece"
        alt="Chess Piece"
        />
    )
}

export default ChessPiece