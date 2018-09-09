/*
	五子棋游戏的界面
	有一个名为lia的联络员在py和qml间传递数据
*/

import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2

Rectangle 
{
	property int n: 15
	property int m: 15
	property int area_size: 50
	property int lef_fix: 50
	property int rig_fix: 50
	property int top_fix: 50
	property int bot_fix: 50

	property int chess_r: area_size / 2

	property variant color_white: "rgba(255,255,255,1)"
	property variant color_black: "rgba(0,0,0,1)"
	property variant color_white_try: "rgba(255,255,255,0.5)"
	property variant color_black_try: "rgba(0,0,0,0.5)"

	property variant color_white_try_bak: "rgba(255,255,255,0.5)"
	property variant color_black_try_bak: "rgba(0,0,0,0.5)"

	property variant player_char: [0,1]			//0 : man , 1 : robit
	property int now: lia.ask_now()

	visible: true
	width: (m-1) * area_size + lef_fix + rig_fix
	height: (n-1) * area_size + top_fix + bot_fix
	//title: qsTr("Hello World")
	id: wind

	function pos_ij_to_xy(i,j)
	{
		return Qt.point(lef_fix + j * area_size , top_fix + i * area_size)
	}

	function now_is_human()
	{
		return player_char[now] == 0
	}

	property bool rob_moving : false
	function ask_move()
	{
		//while(!can.done);

		rob_moving = true
        can.requestPaint()
		if(!now_is_human())
		{
			var ret = lia.get_robot_move()
			move(ret.x , ret.y)
		}
		rob_moving = false
		//else let the mousearea do the work
	}

    property int should_move : 0

	function move(i,j)
	{
		lia.move(i,j)

		now = lia.ask_now()
		ma.visible = now_is_human()

		can.requestPaint()

		var winner = lia.winner()
		if(winner >= 0)
		{
			win(winner)
			return 
		}
	}

	Text
	{
		id: win_text
		x: 0
		y: 0

		text: ""

	}

	function win(winner)
	{
		ma.visible = false
		should_move = 0
		rob_moving = true
		tim.repeat = false

		win_text.visible = true
		win_text.text = "Winner : Player" + String(winner)

	}

	Canvas
	{
		id: can
		//anchors.fill: parent
		x : 0
		y : 0
		width : parent.width
		height : parent.height

		property variant should_draw_try : ma.visible

		function draw_lines()
		{
			var ctx = can.getContext("2d")

			//console.log(top_fix)

			ctx.lineWidth = 1
			ctx.strokeStyle = "black"
			ctx.fillStyle = "black"

			ctx.beginPath();
			for(var i = 0;i < n;i++)
			{

				ctx.moveTo(lef_fix , top_fix + i * area_size)
				ctx.lineTo(wind.width - rig_fix , top_fix + i * area_size)
			}

			for(var i = 0;i < m;i++)
			{
				ctx.moveTo(lef_fix + i * area_size , top_fix)
				ctx.lineTo(lef_fix + i * area_size , wind.height - bot_fix)
			}
			ctx.stroke()
			
		}

		function draw_chess(color,poi)
		{
			var ctx = can.getContext("2d")

			var x = poi.x
			var y = poi.y

			ctx.lineWidth = 1
			ctx.strokeStyle = "black"
			ctx.fillStyle = color

			ctx.beginPath();
			ctx.arc(x, y, chess_r, 0, Math.PI*2);
			ctx.fill(); 
			ctx.stroke();
			//ctx.closePath();
		}

		function draw_cb()
		{
			var ctx = can.getContext("2d")

			for(var i = 0;i < n;i++)
			{
				for(var j = 0;j < m;j++)
				{
					var v = lia.ask_cb(i,j)
					if(v >= 0)
					{
						var poi = pos_ij_to_xy(i,j)
						if(v == 0)
							draw_chess(color_black , poi , ctx)
						else
							draw_chess(color_white , poi , ctx)
					}
				}
			}

			if(lia.now_time() > 0)
			{
				var las = lia.last_move()
				var poi = pos_ij_to_xy(las.x,las.y)
				var x = poi.x
				var y = poi.y

				ctx.lineWidth = 1
				ctx.fillStyle = "red"
				ctx.beginPath();
				ctx.arc(x, y, 3, 0, Math.PI*2);
				ctx.fill(); 
				//ctx.stroke();
			}

		}

		function draw_try_chess(i,j)
		{
			var col = "white"
			if(wind.now == 0)
				col = color_black_try
			else col = color_white_try

			var poi = pos_ij_to_xy(i,j)
			draw_chess(col,poi)
		}

		function paint_base()
		{
			draw_lines()
			draw_cb()
		}

		onPaint:
		{
			clear()
			paint_base()
			if(should_draw_try)
			{
				draw_try_chess(ma.now_i,ma.now_j)
			}
		}

		function clear()
		{
			var ctx = can.getContext("2d")
			ctx.clearRect(0,0,can.width,can.height)
		}
	}


	MouseArea
	{
		id: ma
		visible: now_is_human()
		hoverEnabled: true
		x: 0
		y: 0
		width: parent.width
		height: parent.height

		property int now_i: 0
		property int now_j: 0

		onPositionChanged:
		{
			if(!ma.visible)
				return 

			var now_y = mouse.y - (top_fix - area_size / 2)
			var now_i = Math.floor(now_y / area_size)

			var now_x = mouse.x - (lef_fix - area_size / 2)
			var now_j = Math.floor(now_x / area_size)

			if(!lia.is_good(now_i,now_j))
				return

			ma.now_i = now_i
			ma.now_j = now_j

			can.requestPaint()

		}

		onClicked:
		{
			wind.move(now_i,now_j)
            should_move = 1
		}
	}


    Timer
    {
    	id: tim

        running: true
        interval: 100
        repeat: true

        onTriggered:
        {
            can.requestPaint()

            if((!rob_moving) && (!now_is_human()))
            {
            	should_move += 1
            }

            if(should_move > 0)
            {
                should_move += 1
                win_text.text = "caculating..."
            }

            if(should_move >= 5)
            {//给他绘制的时间

                //can.requestPaint()
                ask_move()
                should_move = 0
                win_text.text = ""
            }
        }

    }
}
