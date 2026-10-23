type ButtonProps = {
    x: number
    y: number
    width: number
    height: number
    gridColumn?: number
    funcOnClick: () => void
    image?: string
}

function Button({x, y, width, height, gridColumn, funcOnClick}: ButtonProps){
    return (
        <div
            className="button"
            onClick={funcOnClick}
            style={{
                left: `${x}%`,
                top: `${y}%`,
                width: `${width}%`,
                height: `${height}%`,
                gridColumn: gridColumn
            }}
        >

        </div>
    )
}

export default Button;